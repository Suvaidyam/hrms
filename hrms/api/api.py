import frappe
import zipfile
import os
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_travel_costing(employee=None, limit=None):
    # If no employee is provided, get the current user's employee ID
    if not employee:
        current_user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": current_user}, "name")

    # Prepare the SQL query with parameterized values
    sql = """
        SELECT 
            TravelCosting.expense_type, 
            TravelCosting.total_amount, 
            Employee.name, 
            Employee.employee_name
        FROM 
            `tabTravel Request` AS Employee 
        LEFT JOIN
            `tabTravel Request Costing` AS TravelCosting
        ON 
            TravelCosting.parent = Employee.name
        WHERE 
            Employee.employee = %s
    """
    
    # Append LIMIT clause if specified
    if limit is not None:
        sql += " LIMIT %s"

    # Execute the query with parameters
    result = frappe.db.sql(sql,as_dict=True)
    
    return result

@frappe.whitelist(allow_guest=True)
def set_remark(remark,dt,dn):
    new_remark = frappe.new_doc('Remarks')
    new_remark.remarks = remark
    new_remark.document_type = dt
    new_remark.document = dn
    new_remark.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def get_workflow_states():
    return frappe.get_all('Workflow State', filters={'custom_show_remarks':1}, pluck='workflow_state_name', ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def show_remark(dt,dn):
    remark_list = frappe.get_list('Remarks', filters={'document_type':dt,'document':dn}, order_by="creation desc", limit_page_length="1",fields=['remarks','closed'],ignore_permissions=True)
    if len(remark_list) > 0 and remark_list[0].closed != 1:
        return [remark_list[0].remarks]
    else:
        return []



def get_timesheet_records():
    # Get the current month and year
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    
    timesheets = frappe.get_list(
        'Employee Monthly Timesheet',
        filters={
            'docstatus': ['!=', 2],
            'month': current_month, 
            'year': current_year  
        },
        fields=['name']
    )
    return timesheets

@frappe.whitelist()
def generate_bulk_timesheet_pdfs():
    timesheets = get_timesheet_records()
    
    # Define the directory for saving PDFs
    temp_dir = frappe.get_site_path('public', 'files', 'employee_monthly_timesheet_pdfs')
    
    # Ensure the directory exists
    os.makedirs(temp_dir, exist_ok=True)
    
    # List to store the file paths
    pdf_files = []
    
    for timesheet in timesheets:
        try:
            # Generate PDF for each Monthly Timesheet
            pdf = frappe.get_print(
                'Employee Monthly Timesheet',  
                timesheet.name,  
                print_format='Monthly Timesheet',  
                as_pdf=True  
            )
            
            # Define the file path
            file_name = f"{timesheet.name}_Timesheet.pdf"
            file_path = os.path.join(temp_dir, file_name)
            
            # Write the PDF to the file
            with open(file_path, 'wb') as f:
                f.write(pdf)
            
            pdf_files.append(file_path)

        except Exception as e:
            frappe.log_error(f"Error generating PDF for {timesheet.name}: {str(e)}", "Generate Bulk Timesheet PDFs")
    
    # Create ZIP file with the updated name
    zip_file_path = os.path.join(temp_dir, 'Employee_Monthly_Timesheet.zip')
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):  # Ensure the file exists
                zipf.write(pdf_file, os.path.basename(pdf_file))
                os.remove(pdf_file)  # Remove the file after adding it to the ZIP

    # Save the ZIP file in the `File` Doctype with the updated name
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "Employee_Monthly_Timesheet.zip",
        "file_url": f"/files/employee_monthly_timesheet_pdfs/Employee_Monthly_Timesheet.zip",
        "is_private": 1,  
    })
    file_doc.insert(ignore_permissions=True)
    
    # Return the file document info
    return {
        "message": "ZIP file created and saved successfully",
        "file_url": file_doc.file_url,
        "file_name": file_doc.file_name
    }



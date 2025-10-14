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



import os, zipfile
import frappe
from datetime import datetime
today = datetime.today()
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf


def get_timesheet_records(year,month):
    timesheets = frappe.get_list(
        'Employee Monthly Timesheet',
        filters={
            'docstatus': ['!=', 2],
            'month': month, 
            'year': year  
        },
        fields=['name']
    )
    return timesheets


@frappe.whitelist()
def generate_bulk_timesheet_pdfs(year=None, month=None):
    try:
        doc = frappe.get_doc({
            "doctype": "Bulk Monthly Timesheet",
            "user": frappe.session.user,
            "request_date": frappe.utils.now_datetime(),
            "month": month,
            "year": year,
            "status": "Pending",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.enqueue(
            background_timesheet_pdfs,
            year=year,
            month=month,
            record_name=doc.name,
            queue="long",
            timeout=3600,
            job_id=f"Generate Timesheet pdf {year}-{month}"  # Unique job ID to prevent duplicates
        )
        return {"message": "Bulk generation started", "record": doc.name}
    except Exception as e:
        frappe.log_error(f"Failed to create Bulk Timesheet record: {str(e)}", "Bulk Monthly Timesheet")
        return {"error": str(e)}




@frappe.whitelist()
def background_timesheet_pdfs(year=None, month=None,record_name=None):
    frappe.log_error(
        f"Starting bulk Monthly Timesheet generation | Year: {year}, Month: {month}",
        "Bulk Monthly Timesheet  Generation"
    )
    year = frappe.utils.cint(year)   # convert to int
    month = frappe.utils.cint(month)
    
    if not year or not month:
        today = datetime.today()
        year = today.year
        month = today.month
    # fetch timesheets
    timesheets = get_timesheet_records(year, month)  
    if not timesheets:
        _update_bulk_record(record_name, "Failed", None)
        return {"message": "No timesheets found for current month"}
    
    _update_bulk_record(record_name, "Processing")

    temp_dir = frappe.get_site_path('private', 'files')
    os.makedirs(temp_dir, exist_ok=True)
    
    for f in os.listdir(temp_dir):
        if f.startswith("Employee_Monthly_Timesheet") and (f.endswith(".pdf") or f.endswith(".zip")):
            try:
                os.remove(os.path.join(temp_dir, f))
            except Exception as e:
                frappe.log_error(f"Failed to delete old file {f}: {str(e)}", "Generate Bulk Timesheet PDFs Cleanup")
    
    pdf_files = []

    for timesheet in timesheets:
        frappe.log_error(f"Generating PDF for {timesheet.name}", "Bulk monthly timeSheet Generation")
        doc = frappe.get_doc("Employee Monthly Timesheet", timesheet.name)
        try:
          
            print_format = frappe.get_doc("Print Format", "Monthly Timesheet")
            pdf_template = print_format.html
            css = print_format.css or ""

            # Render HTML using Jinja
            html_content = frappe.render_template(pdf_template, {"doc": doc})
            full_html = f"<style>{css}</style>{html_content}"

            pdf_bytes = get_pdf(full_html)

            # Save PDF temporarily
            filename = f"{doc.name}.pdf"
            file_path = os.path.join(get_site_path("private", "files"), filename)

            with open(file_path, 'wb') as f:
                f.write(pdf_bytes)

            pdf_files.append(file_path)

        except Exception as e:
            frappe.log_error(f"Error generating PDF for {timesheet.name}: {str(e)}", "Generate Bulk Timesheet PDFs")
    
    # Create a ZIP file
    zip_filename = f"Employee_Monthly_Timesheet_{month}_{year}_.zip"
    zip_file_path = os.path.join(temp_dir, zip_filename)
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                zipf.write(pdf_file, os.path.basename(pdf_file))
                os.remove(pdf_file)  # cleanup

    # Attach the ZIP to File Doctype (private)
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": zip_filename,
        "file_url": f"/private/files/{zip_filename}",
        "is_private": 1,
    })
    file_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    _update_bulk_record(record_name, "Complete", file_doc.file_url)
    os.remove(zip_file_path)
    return {
        "message": "ZIP file created and saved successfully",
        "file_url": file_doc.file_url,
        "file_name": file_doc.file_name
    }


def _update_bulk_record(record_name, status, file_url=None):
    """Helper to safely update Bulk Monthly Timesheet record."""
    try:
        if not record_name:
            return
        doc = frappe.get_doc("Bulk Monthly Timesheet", record_name)
        doc.status = status
        if file_url:
            doc.url_autogenerated_file = file_url
        doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Failed to update Bulk Timesheet record {record_name}: {str(e)}", "Bulk Monthly Timesheet Update")

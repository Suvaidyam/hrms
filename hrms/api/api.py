import frappe

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

# from frappe import _
# @frappe.whitelist()
# def notify_reports_to():
#     # Get the Employee record linked to the current user
#     current_user_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
#     if not current_user_employee:
#         frappe.throw("No Employee record is linked to the current user.")
    
#     # Get the reports_to for the current user's Employee record
#     reports_to = frappe.db.get_value("Employee", current_user_employee, "reports_to")
#     print("Reports to==================================",reports_to)
#     if not reports_to:
#         frappe.throw("The current user does not have a 'reports_to' defined.")
    
#     # Fetch the name and email of the reports_to employee
#     reports_to_name = frappe.db.get_value("Employee", reports_to, "employee_name")
#     reports_to_email = frappe.db.get_value("Employee", reports_to, "user_id")
    
#     if not reports_to_email:
#         frappe.throw("The 'reports_to' employee does not have an email ID.")
    
#     # Prepare the email content
#     subject = "Notification: Action Required"
#     message = f"""
#     Dear {reports_to_name},

#     The current logged-in user ({frappe.session.user}) has identified you as their reporting manager.
#     This is a system notification to ensure awareness and communication.

#     Regards,
#     System
#     """
    
#     # Send email
#     frappe.sendmail(
#         recipients=[reports_to_email],
#         subject=subject,
#         message=message
#     )
    
#     return {"message": f"Email sent to {reports_to_name} at {reports_to_email}"}

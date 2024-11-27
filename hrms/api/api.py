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
# @frappe.whitelist(allow_guest=True)
# def send_travel_request_email(docname):
    print('==================================== ewfnejfnejfer')
    # Fetch the document
    doc = frappe.get_doc("Travel Request", docname)
    print(doc,'doc==========================')
    # Get the Team Leader (TL) of the employee
    TL = frappe.db.get_value("Employee", doc.employee, "reports_to")
    print('==========================================TL', TL)
    if TL:
        TL_name = frappe.db.get_value("Employee", TL, "employee_name")
        TL_email = frappe.db.get_value("Employee", TL, "user_id")
        print('============================================= Tl_email',TL_name)
        print('============================================= Tl_email',TL_email)
        if TL_email:
            subject = f"Travel Request Pending for Your Approval - {doc.name}"
            message = f"""
            Dear {TL_name},

            A new travel request ({doc.name}) has been submitted by {doc.employee_name}.
            Please review and take the necessary action.

            Regards,
            System
            """
            frappe.sendmail(recipients=[TL_email], subject=subject, message=message)
    
    # Get the CEO (reports_to of TL)
    Ceo = frappe.db.get_value("Employee", TL, "reports_to") if TL else None
    if Ceo:
        Ceo_name = frappe.db.get_value("Employee", Ceo, "employee_name")
        Ceo_email = frappe.db.get_value("Employee", Ceo, "user_id")
        print(Ceo_email,'===================================================Ceo_email')
        if Ceo_email:
            subject = f"Travel Request Pending for Your Approval - {doc.name}"
            message = f"""
            Dear {Ceo_name},

            A travel request ({doc.name}) has been approved by {TL_name} and is now pending your approval.

            Regards,
            System
            """
            frappe.sendmail(recipients=[Ceo_email], subject=subject, message=message)

    # Send email to the employee regardless of workflow state
    employee_email = frappe.db.get_value("Employee", doc.employee, "user_id")
    if employee_email:
        subject = f"Update on Your Travel Request - {doc.name}"
        message = f"""
        Dear {doc.employee_name},

        Your travel request ({doc.name}) is currently under review.
        Please monitor the progress and take any necessary action as per the workflow.

        Regards,
        System
        """
        frappe.sendmail(recipients=[employee_email], subject=subject, message=message)
    
    return {"status": "success", "message": _("Emails sent successfully.")}

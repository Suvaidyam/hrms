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
def show_remark(dt,dn):
    remark_list = frappe.get_list('Remarks', filters={'document_type':dt,'document':dn}, order_by="creation desc", limit_page_length="1",pluck='remarks',ignore_permissions=True)
    # print('=================================================',remark_list)
    return remark_list



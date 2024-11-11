import frappe

def get_permission_query_conditions_for_expense_claim(user):
    user = frappe.session.user  # Get the logged-in user

    # if "System Manager" in frappe.get_roles(user):
    #     return None 
    
    # else:
    return f"""(
            `tabExpense Claim`.owner = '{user}' 
            OR `tabExpense Claim`.workflow_state != 'Draft'
        )"""


def get_permission_query_conditions_for_travel_request(user):
    if not user: user = frappe.session.user

    # if "System Manager" in frappe.get_roles(user):
    #     return None
    # else:
    return """(`tabTravel Request`.workflow_state != 'Draft')"""

def get_permission_query_conditions_for_leave_request(user):
    if not user: user = frappe.session.user

    # if "System Manager" in frappe.get_roles(user):
    #     return None
    # else:
    return """(`tabLeave Application`.workflow_state != 'Draft')"""
    

def get_permission_query_conditions_for_attendance_request(user):
    if not user: user = frappe.session.user

    # if "System Manager" in frappe.get_roles(user):
    #     return None
    # else:
    return """(`tabAttendance Request`.workflow_state != 'Draft')"""
    

def get_permission_query_conditions_for_timesheet_request(user):
    if not user: user = frappe.session.user

    # if "System Manager" in frappe.get_roles(user):
    #     return None
    # else:
    return """(`tabEmployee Monthly Timesheet`.workflow_state != 'Draft')"""
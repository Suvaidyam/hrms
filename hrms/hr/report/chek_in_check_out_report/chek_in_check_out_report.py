# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"fieldname": "employee",
			"fieldtype": "Data",
			"label": "Employee Code",
		},
		{
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"label": "Employee Name",
		},
		{
			"fieldname": "designation",
			"fieldtype": "Data",
			"label": "Designation",
		},
		{
			"fieldname": "checkin",
			"fieldtype": "Data",
			"label": "Check In",
		},
		{
			"fieldname": "checkout",
			"fieldtype": "Data",
			"label": "Check Out",
		},
		{
			"fieldname": "in_count",
			"fieldtype": "Int",
			"label": "Count (In)",
		},
		{
			"fieldname": "out_count",
			"fieldtype": "Int",
			"label": "Count (Out)",
		},
		{
			"fieldname": "location",
			"fieldtype": "Data",
			"label": "Location In Time",
		}
		]
	sql_query = """
			SELECT
				t.employee,
				e.employee_name,
				e.designation,
				t.checkin,
				t.checkout,
				(CASE WHEN t.in_count > 0 THEN 1 ELSE 0 END) AS in_count,
				(CASE WHEN t.out_count > 0 THEN 1 ELSE 0 END) AS out_count,
				CONCAT(t.latitude, ',', t.longitude) AS location
			FROM 
				(SELECT
					employee,
					latitude,
					longitude,
					DATE(MIN(CASE WHEN log_type = 'IN' THEN time END)) AS date,
					TIME_FORMAT(MIN(CASE WHEN log_type = 'IN' THEN time END), '%H:%i:%s') AS checkin,
					TIME_FORMAT(MAX(CASE WHEN log_type = 'OUT' THEN time END), '%H:%i:%s') AS checkout,
					SUM(CASE WHEN log_type = 'IN' THEN 1 ELSE 0 END) AS in_count,
					SUM(CASE WHEN log_type = 'OUT' THEN 1 ELSE 0 END) AS out_count
				FROM
					`tabEmployee Checkin` ec
				WHERE
					DATE(time) = CURRENT_DATE()
				GROUP BY
					employee, DATE(time)
				ORDER BY
					MIN(CASE WHEN log_type = 'IN' THEN time END) ASC, employee) t
			LEFT JOIN 
				`tabEmployee` AS e 
			ON 
				e.name = t.employee;

	""" 
	data = frappe.db.sql(sql_query)
	return columns, data

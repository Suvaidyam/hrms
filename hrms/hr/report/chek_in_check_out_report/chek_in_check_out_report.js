// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Chek-In Check-Out Report"] = {
	"filters": [

	],
	formatter: function (value, k, column) {
		if (column.fieldname == 'location') {
			return `<a target="_blank" href="https://www.google.com/maps?q=${value}">________<i class="fa fa-map-marker" style="font-size:19px">______</i></a>`
		}
		return `<span>${value}</span>`
	}
};

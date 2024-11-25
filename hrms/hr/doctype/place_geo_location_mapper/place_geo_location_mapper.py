# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PlaceGeoLocationMapper(Document):
	def validate(self):
		if not frappe.db.get_single_value("HR Settings", "allow_geolocation_tracking"):
			frappe.throw("Geo Location Tracking is not Enable")
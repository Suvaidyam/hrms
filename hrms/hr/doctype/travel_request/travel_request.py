# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from frappe.model.document import Document
import frappe

from hrms.hr.utils import validate_active_employee

@frappe.whitelist()
def get_itinerary(employee, itinerary_id=None):
	itinerary = frappe.qb.DocType("Travel Itinerary")

	query = frappe.qb.from_(itinerary).select(
		itinerary.name,
		itinerary.travel_from,
		itinerary.travel_to,
		itinerary.mode_of_travel,
		itinerary.meal_preference,
		itinerary.departure_date,
		itinerary.arrival_date,
	)

	if not itinerary_id:
		query = query.where(
			(itinerary.docstatus == 1)
			& (itinerary.employee == employee)
			& (itinerary.paid_amount > 0)
			& (itinerary.status.notin(["Claimed", "Returned", "Partly Claimed and Returned"]))
		)
	else:
		query = query.where(itinerary.name == itinerary_id)

	return query.run(as_dict=True, ignore_permissions=True)


class TravelRequest(Document):
	def validate(self):
		validate_active_employee(self.employee)


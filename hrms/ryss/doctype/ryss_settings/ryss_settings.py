# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import os, zipfile

class RySSSettings(Document):
	def get_os_intance(self):
		return os

	def listdirectory(self,path):
		print("Path:===============================",path)
		return os.listdir(path)

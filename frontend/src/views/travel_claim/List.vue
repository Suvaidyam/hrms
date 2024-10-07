<template>
	<ion-page>
		<ListView
			doctype="Expense Claim"
			pageTitle="Travel History"
			:tabButtons="TAB_BUTTONS"
			:fields="TRAVEL_CLAIM_FIELDS"
			:filterConfig="FILTER_CONFIG"
		/>
	</ion-page>
</template>

<script setup>
import { IonPage } from "@ionic/vue"
import ListView from "@/components/ListView.vue"

const TAB_BUTTONS = ["My Claims", "Team Claims"]
const TRAVEL_CLAIM_FIELDS = [
	"`tabExpense Claim`.name",
	"`tabExpense Claim`.employee",
	"`tabExpense Claim`.employee_name",
	"`tabExpense Claim`.approval_status",
	"`tabExpense Claim`.status",
	"`tabExpense Claim`.expense_approver",
	"`tabExpense Claim`.total_claimed_amount",
	"`tabExpense Claim`.posting_date",
	"`tabExpense Claim`.company",
	"`tabExpense Claim Detail`.expense_type",
	"count(`tabExpense Claim Detail`.expense_type) as total_expenses",

	// "`tabTravel Request`.name",
	// 	"`tabTravel Request`.travel_type",
	// 	"`tabTravel Request`.purpose_of_travel",
	// 	"`tabTravel Request`.employee_name",
	// 	"`tabTravel Request`.cell_number",
	// 	"`tabTravel Request Costing`.expense_type",
	// 	"count(`tabTravel Request Costing`.expense_type) as total_expenses",
]

const FILTER_CONFIG = [
	// {
	// 	fieldname: "approval_status",
	// 	fieldtype: "Select",
	// 	label: "Approval Status",
	// 	options: ["Draft", "Approved", "Rejected"],
	// },
	{
		fieldname: "status",
		fieldtype: "Select",
		label: "Status",
		options: ["Draft", "Paid", "Unpaid", "Rejected", "Submitted", "Cancelled"],
	},
	{
		fieldname: "employee",
		fieldtype: "Link",
		label: "Employee",
		options: "Employee",
	},
	{
		fieldname: "department",
		fieldtype: "Link",
		label: "Department",
		options: "Department",
	},
	{ fieldname: "posting_date", fieldtype: "Date", label: "Posting Date" },
]
</script>

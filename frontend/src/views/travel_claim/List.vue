<template>
	<ion-page>
		<ListView
			doctype="Travel Request"
			pageTitle="Claim Travel Request History"
			:tabButtons="TAB_BUTTONS"
			:fields="EXPENSE_CLAIM_FIELDS"
			groupBy="`tabTravel Request`.name"
			:filterConfig="FILTER_CONFIG"
		/>
	</ion-page>
</template>

<script setup>
import { IonPage } from "@ionic/vue"
import ListView from "@/components/ListView.vue"

const TAB_BUTTONS = ["My Claims", "Team Claims"]
const EXPENSE_CLAIM_FIELDS = [
	"`tabTravel Request`.name",
	"`tabTravel Request`.employee",
	"`tabTravel Request`.employee_name",
	// "`tabTravel Request`.approval_status",
	"`tabTravel Request`.status",
	"`tabTravel Request`.expense_approver",
	"`tabTravel Request`.total_claimed_amount",
	// "`tabTravel Request`.posting_date",
	"`tabTravel Request`.company",
	"`tabTravel Request Detail`.travel_type",
	"count(`tabTravel Request Detail`.travel_type) as total_expenses",
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

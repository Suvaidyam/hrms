// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Bulk Monthly Timesheet", {
// 	refresh(frm) {

// 	},
// });
// Copyright (c) 2025, kallu
// For license information, please see license.txt

frappe.ui.form.on("Bulk Monthly Timesheet", {
	refresh(frm) {
		if (frm.doc.status !== "Completed") {
			frappe.realtime.on("bulk_timesheet_progress", (data) => {
				if (data.record === frm.doc.name) {
					frm.set_value("track_records", data.progress);
					frm.refresh_field("track_records");
				}

				frappe.show_progress(
					"Generating Timesheets...",
					data.generated,
					data.total,
					`${data.generated} of ${data.total} completed (${data.failed} failed)`
				);

				if (data.generated + data.failed === data.total) {
					frappe.hide_progress();
					setTimeout(() => frm.reload_doc(), 1000);
				}
			});
		}
	},
});

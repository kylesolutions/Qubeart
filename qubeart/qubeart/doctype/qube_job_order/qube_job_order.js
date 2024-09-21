// Copyright (c) 2024, Vivek and contributors
// For license information, please see license.txt

frappe.ui.form.on('Qube Job Order', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 0){
			frm.add_custom_button(__("Create Stock Issue"), function () {
				frappe.confirm('Are you sure you want to Create Stock Issue for Raw  Materials ?',
					() => {
						frappe.xcall("qubeart.qubeart.doctype.qube_job_order.qube_job_order.make_stock_entry", {
							qube_job_order_id: frm.doc.name,
							purpose: "Material Issue"
						}).then((stock_entry) => {
						frappe.model.sync(stock_entry);
						frappe.set_route("Form", stock_entry.doctype, stock_entry.name);
					});
					}, 
					() => {
						// action to perform if No is selected
					}
				)
			});
		}
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Create Stock Receipt"), function () {
				frappe.confirm('Are you sure you want to Create Stock Receipt for Production Item ?',
					() => {
						frappe.xcall("qubeart.qubeart.doctype.qube_job_order.qube_job_order.make_stock_entry", {
							qube_job_order_id: frm.doc.name,
							purpose: "Material Receipt"
						}).then((stock_entry) => {
						frappe.model.sync(stock_entry);
						frappe.set_route("Form", stock_entry.doctype, stock_entry.name);
					});
					}, 
					() => {
						// action to perform if No is selected
					}
				)
			});
		}
	}
});

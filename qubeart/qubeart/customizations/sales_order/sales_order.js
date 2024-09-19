frappe.ui.form.on("Sales Order",{
    refresh:function(frm){
        if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Qube Job Order"), function () {
				frappe.model.open_mapped_doc({
					method: "qubeart.qubeart.customizations.sales_order.sales_order.job_order_creation",
					frm: frm,
				});
			});
		}
    }

})
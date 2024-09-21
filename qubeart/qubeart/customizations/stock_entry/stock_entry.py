import frappe

def on_submit(self, method = None):
    if self.custom_qube_job_order and self.purpose == "Material Issue":
        qube_job_order = frappe.get_doc("Qube Job Order", self.custom_qube_job_order)
        item = [i.item_code for i in qube_job_order.raw_materials ]
        for i in self.items:
            if i.item_code not in item:
                qube_job_order.append("raw_materials", dict(
                    warehouse = i.s_warehouse,
				    item_code = i.item_code,
				    qty = i.qty,
				    uom = i.uom,
                ))
        qube_job_order.save()
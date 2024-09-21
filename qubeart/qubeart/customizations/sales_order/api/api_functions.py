from frappe.utils import today
from frappe import _

import frappe
from frappe.model.mapper import get_mapped_doc
import json


def make_doc(item_details,customer,name,customer_name):
	exists_job_order= frappe.db.get_all("Qube Job Order",{"sales_order":name})
	if exists_job_order:
		frappe.msgprint(_("Aleady Qube Job Order Created Against {0}").format(name))
	else:
		item_details=json.loads(item_details)
		for i in item_details:
			job_order_doc=frappe.new_doc("Qube Job Order")
			job_order_doc.customer=customer
			job_order_doc.customer_name=customer_name
			job_order_doc.date=today()
			job_order_doc.sales_order=name 
			job_order_doc.append("production_item",{
				"item_code": i.get("item_code"),
				"item_name": i.get("item_name"),
				"description": i.get("description"),
				"uom": i.get("uom"),
				"qty": i.get("qty"),
				"warehouse":i.get("warehouse"),
				"frame_length": i.get("frame_length"),
				"frame_breadth": i.get("frame_breadth"),
			})
			job_order_doc.save(ignore_permissions=True)

from frappe.utils import today


import frappe
from frappe.model.mapper import get_mapped_doc



def make_doc(source_name, target_doc):
	def postprocess(source, target):
		set_missing_values(source, target)

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	doc = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Qube Job Order",
				"field_map": {
					
					"name":"sales_order",
					"customer": "customer",
     				today(): "date",
				},
			},
			"Sales Order Item": {
				"doctype": "Qube Production Item",
				"field_map": {
					"item_code": "item_code",
					"item_name": "item_name",
					"description": "description",
					"uom": "uom",
					"qty": "qty",
					"custom_frame_length": "frame_length",
					"custom_frame_breadth": "frame_breadth",
				},
			},
		},
		target_doc,
		postprocess,
	)
	doc.save(ignore_permissions=True)
	return doc
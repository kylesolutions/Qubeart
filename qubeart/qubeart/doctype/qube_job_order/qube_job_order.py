# Copyright (c) 2024, Vivek and contributors
# For license information, please see license.txt

import frappe
import math
from frappe import _

from frappe.model.document import Document

class QubeJobOrder(Document):
	def validate(self):
		self.calculate_qty()
	
	def calculate_qty(self):
		frame_length = 0
		frame_breadth = 0
		for item in self.production_item:
			frame_length += item.frame_length or 0
			frame_breadth += item.frame_breadth or 0
		for item in self.raw_materials:
			if item.is_frame == 1:
				frames_length = math.ceil(item.default_size / frame_length)
				frames_breadth = math.ceil(item.default_size / frame_breadth)
				item.qty = frames_length + frames_breadth
				item.usage_qty = (2*frame_length) + (2*frame_breadth)
				item.scrap_qty = (item.qty*item.default_size) - item.usage_qty


@frappe.whitelist()
def make_stock_entry(qube_job_order_id, purpose):
	exists_stock_entry= frappe.db.get_all("Stock Entry",{"custom_qube_job_order":qube_job_order_id, "purpose": purpose})
	if exists_stock_entry:
		frappe.throw(_("Aleady Stock Entry Created Against {0}").format(qube_job_order_id))
	qube_job_order = frappe.get_doc("Qube Job Order", qube_job_order_id)

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.purpose = purpose
	stock_entry.custom_qube_job_order = qube_job_order_id
	stock_entry.company = qube_job_order.company

	if purpose == "Material Issue":
		for item in qube_job_order.raw_materials:
			stock_entry.append("items",dict(
				s_warehouse = item.warehouse,
				item_code = item.item_code,
				qty = item.qty,
				uom = item.uom,
				stock_uom = frappe.get_value("Item", item.item_code,"stock_uom")
			))
	elif purpose == "Material Receipt":
		for item in qube_job_order.production_item:
			stock_entry.append("items",dict(
				t_warehouse = item.warehouse,
				item_code = item.item_code,
				qty = item.qty,
				uom = item.uom,
				stock_uom = frappe.get_value("Item", item.item_code,"stock_uom")
			))
	stock_entry.set_stock_entry_type()
	stock_entry.save()
	return stock_entry.as_dict()

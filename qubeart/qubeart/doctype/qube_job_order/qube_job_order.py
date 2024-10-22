# Copyright (c) 2024, Vivek and contributors
# For license information, please see license.txt

import frappe
import math
from frappe import _
from frappe.utils import (
	get_link_to_form,
)

from frappe.model.document import Document

class QubeJobOrder(Document):
	def validate(self):
		self.calculate_qty()
	
	def calculate_qty(self):
		frame_length = 0
		frame_breadth = 0
		num_frames = 1
		for item in self.production_item:
			frame_length += item.frame_length or 0
			frame_breadth += item.frame_breadth or 0
			num_frames = item.qty
		for item in self.raw_materials:
			if item.is_frame == 1:
				# frames_length = math.ceil(item.default_size / frame_length)
				# frames_breadth = math.ceil(item.default_size / frame_breadth)
				# item.qty = frames_length + frames_breadth
				# if frame_length <= (item.default_size - frame_length):
				# 	item.qty = 1
				# else:
				# 	item.qty = 2
				# if frame_breadth <= (item.default_size - frame_breadth):
				# 	item.qty += 1
				# else:
				# 	item.qty += 2
				# item.usage_qty = (2*frame_length) + (2*frame_breadth)
				# item.scrap_qty = (item.qty*item.default_size) - item.usage_qty
				single_frame_size = (2 * frame_length) + (2 * frame_breadth)

				# Total size required for all frames
				total_piece_size = single_frame_size * num_frames

				# Calculate how many units of default_size are needed
				if total_piece_size <= item.default_size:
					item.qty = 1  # 1 qty is enough for all the pieces
				else:
					item.qty = math.ceil(total_piece_size / item.default_size)

				# Set usage and scrap quantities
				item.usage_qty = total_piece_size
				item.scrap_qty = (item.qty * item.default_size) - item.usage_qty

@frappe.whitelist()
def make_stock_entry(qube_job_order_id, purpose):
	exists_stock_entry= frappe.db.get_all("Stock Entry",{"custom_qube_job_order":qube_job_order_id, "purpose": purpose})
	if exists_stock_entry:
		frappe.throw(_("Aleady Stock Entry {1} Created Against {0}").format(qube_job_order_id,get_link_to_form("Stock Entry", exists_stock_entry[0].name)))
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
		scrap_stock_entry = frappe.new_doc("Stock Entry")
		scrap_stock_entry.purpose = "Material Receipt"
		scrap_stock_entry.custom_qube_job_order = qube_job_order_id
		scrap_stock_entry.company = qube_job_order.company
		for item in qube_job_order.raw_materials:
			if item.is_frame == 1:
				for _ in range(item.qty):
					scrap_stock_entry.append("items", dict(
						t_warehouse=item.scrap_warehouse,
						item_code=item.item_code,
						qty=1,
						uom=item.uom,
						stock_uom=frappe.get_value("Item", item.item_code, "stock_uom")
					))
				scrap_stock_entry.set_stock_entry_type()
				scrap_stock_entry.save(ignore_permissions=True)
  
	stock_entry.set_stock_entry_type()
	stock_entry.save(ignore_permissions=True)
	return stock_entry.as_dict()

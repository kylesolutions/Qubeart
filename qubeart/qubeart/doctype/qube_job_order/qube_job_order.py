# Copyright (c) 2024, Vivek and contributors
# For license information, please see license.txt

import frappe
import math

from frappe.model.document import Document

class QubeJobOrder(Document):
	def validate(self):
		self.calculate_qty()
	
	def calculate_qty(self):
		frame_length = 0
		frame_breadth = 0
		for item in self.production_item:
			frame_length += item.frame_length 
			frame_breadth += item.frame_breadth
		for item in self.raw_materials:
			if item.is_frame == 1:
				frames_length = math.ceil(item.default_size / frame_length)
				frames_breadth = math.ceil(item.default_size / frame_breadth)
				item.qty = frames_length + frames_breadth
				item.usage_qty = (2*frame_length) + (2*frame_breadth)
				item.scrap_qty = (item.qty*item.default_size) - item.usage_qty


		

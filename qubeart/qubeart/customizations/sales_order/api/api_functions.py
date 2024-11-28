from frappe.utils import today
from frappe import _

import frappe
from frappe.model.mapper import get_mapped_doc
import json


def make_doc(item_details,customer,name,customer_name,po_no,delivery_date):
	exists_job_order= frappe.db.get_all("Qube Job Order",{"sales_order":name})
	if exists_job_order:
		frappe.msgprint(_("Aleady Qube Job Order Created Against {0}").format(name))
	else:
		item_details=json.loads(item_details)
		for i in item_details:
			job_order_doc=frappe.new_doc("Qube Job Order")
			job_order_doc.customer=customer
			job_order_doc.customer_name=customer_name
			job_order_doc.delivery_date=delivery_date
			job_order_doc.customers_purchase_order=po_no
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
    			"customer_artwork":i.get("customer_artwork"),
				"types_of_job":i.get("types_of_job"),
				"image_size":i.get("image_size"),
				"border":i.get("border"),				
    			"mirror":i.get("mirror"),				
       			"gallery_wrap_edge":i.get("gallery_wrap"),
          		"frame_code_1":i.get("frame_code1"),				
            	"frame_code_2":i.get("frame_code2"),	
				"frame_code_3":i.get("frame_code3"),
    			"frame_code_1_balance":i.get("frame_code1_balance"),
       			"frame_code_2_balance":i.get("frame_code2_balance"),
				"frame_code_3_balance":i.get("frame_code3_balance"),
             	"mount_code_1":i.get("mount_code1"),				
              	"mount_code_2":i.get("mount_code2"),
				"mount_code_3":i.get("mount_code3"),
				"mount_code_1_balance":i.get("mount_code1_balance"),
				"mount_code_2_balance":i.get("mount_code2_balance"),
				"mount_code_3_balance":i.get("mount_code3_balance"),	
               	"glass":i.get("glass"),				
                "drymount":i.get("drymount"),				
                "hanging_system":i.get("hanging_system"),
			})
			for item in ["frame_code1", "frame_code2", "frame_code3", "mount_code1", "mount_code2", "mount_code3"]:
				if i.get(item):  # Ensure the item_code is not None
					job_order_doc.append("raw_materials", {
						"item_code": i.get(item)
					})
			job_order_doc.save(ignore_permissions=True)

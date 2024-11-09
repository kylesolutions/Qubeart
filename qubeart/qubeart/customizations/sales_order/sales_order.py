from qubeart.qubeart.customizations.sales_order.api.api_functions import (
    make_doc,
)
import frappe


@frappe.whitelist()
def job_order_creation(item_details,customer,name,customer_name,po_no,delivery_date):
    return make_doc(item_details,customer,name,customer_name,po_no,delivery_date)
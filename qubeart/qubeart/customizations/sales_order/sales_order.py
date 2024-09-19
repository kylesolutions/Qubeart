from qubeart.qubeart.customizations.sales_order.api.api_functions import (
    make_doc,
)
import frappe


@frappe.whitelist()
def job_order_creation(source_name, target_doc=None):
    return make_doc(source_name, target_doc=None)
import frappe
from frappe.utils import add_days, today
from qubeart.qubeart.doctype.emaar_daily_sales.emaar_daily_sales import send_emaar_data

def emaar_daily_sales_automatic_creation():
    doc = frappe.new_doc("Emaar Daily Sales")
    doc.date = utils.today()
    doc.insert(ignore_permissions=True)
    doc.save()
    doc.submit()

def emaar_data_Send():
    yesterday = add_days(today(), -1)
    daily_sales = frappe.get_all(
        "Emaar Daily Sales",
        {"docstatus": 1, "date": yesterday},
        "name"
    )
    for sales in daily_sales:
        send_emaar_data(sales.name)
            
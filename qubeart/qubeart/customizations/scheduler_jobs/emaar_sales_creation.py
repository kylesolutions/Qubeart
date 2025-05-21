import frappe
from frappe.utils import add_days, today
from qubeart.qubeart.doctype.emaar_daily_sales.emaar_daily_sales import send_emaar_data
from datetime import datetime, timedelta
import calendar

from qubeart.qubeart.doctype.monthly_sales_emaar.monthly_sales_emaar import send_emaar_data as emaar_monthly_send_data
def emaar_daily_sales_automatic_creation():
    doc = frappe.new_doc("Emaar Daily Sales")
    doc.date = today()
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
            


def create_and_send_emaar_monthly_sales():
    today = datetime.today()
    first_day_last_month = today.replace(day=1) - timedelta(days=1)
    from_date = first_day_last_month.replace(day=1)
    to_date = first_day_last_month.replace(day=calendar.monthrange(first_day_last_month.year, first_day_last_month.month)[1])

    doc = frappe.new_doc("Monthly Sales Emaar")
    doc.from_date = from_date
    doc.to_date = to_date
    doc.insert(ignore_permissions=True)
    doc.submit()
    
    emaar_monthly_send_data(doc.name)
import frappe

def validate(doc, method):
    if not doc.date:
        frappe.throw("Please select a date.")

    # Fetch all submitted Sales Invoices for the selected date
    sales_invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "posting_date": doc.date,
            "docstatus": 1  # Only submitted invoices
        },
        fields=["name", "total"]
    )

    total_sales = 0
    for invoice in sales_invoices:
        # Get VAT (if any) from the child table
        vat_amount = 0
        taxes = frappe.get_all(
            "Sales Taxes and Charges",
            filters={"parent": invoice.name},
            fields=["tax_amount"]
        )
        for tax in taxes:
            vat_amount += tax.tax_amount

        net_sales = invoice.total - vat_amount
        total_sales += net_sales

    doc.total_sales = total_sales
    doc.total_invoice = len(sales_invoices)

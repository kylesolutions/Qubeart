// Copyright (c) 2025, Vivek and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Job Order Status"] = {
  "filters": [
    {
      "fieldname": "from_date",
      "label": "From Date",
      "fieldtype": "Date",
      "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
      "reqd": 1
    },
    {
      "fieldname": "to_date",
      "label": "To Date",
      "fieldtype": "Date",
      "default": frappe.datetime.get_today(),
      "reqd": 1
    },
    {
      "fieldname": "qc_status",
      "label": "QC Status",
      "fieldtype": "Select",
      "options": "\nPass\nFail",
      "default": ""
    },
    {
      "fieldname": "production_status",
      "label": "Production Status",
      "fieldtype": "Select",
      "options": "\nProduction Start\nProduction In Progress\nProduction Completed\nQC Check",
      "default": ""
    }
  ]
};

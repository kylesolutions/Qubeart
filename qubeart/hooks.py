app_name = "qubeart"
app_title = "Qubeart"
app_publisher = "Vivek"
app_description = "Custom Development"
app_email = "vivekchamp84@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/qubeart/css/qubeart.css"
# app_include_js = "/assets/qubeart/js/qubeart.js"

# include js, css files in header of web template
# web_include_css = "/assets/qubeart/css/qubeart.css"
# web_include_js = "/assets/qubeart/js/qubeart.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "qubeart/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Order" : "qubeart/customizations/sales_order/sales_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "qubeart.utils.jinja_methods",
# 	"filters": "qubeart.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "qubeart.install.before_install"
# after_install = "qubeart.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "qubeart.uninstall.before_uninstall"
# after_uninstall = "qubeart.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "qubeart.utils.before_app_install"
# after_app_install = "qubeart.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "qubeart.utils.before_app_uninstall"
# after_app_uninstall = "qubeart.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "qubeart.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry": {
		"on_submit": "qubeart.qubeart.customizations.stock_entry.stock_entry.on_submit",
	},
	"Emaar Daily Sales": {
        "validate": "qubeart.qubeart.doctype.emaar_daily_sales.emaar_daily_sales.validate"
    },
	"Monthly Sales Emaar": {
        "validate": "qubeart.qubeart.doctype.monthly_sales_emaar.monthly_sales_emaar.validate"
    }
}


# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"59 23 * * *": [
			"qubeart.qubeart.customizations.scheduler_jobs.emaar_sales_creation.emaar_daily_sales_automatic_creation"
		],
		"0 6 * * *": [
			"qubeart.qubeart.customizations.scheduler_jobs.emaar_sales_creation.emaar_data_Send"
		],
		 "0 1 1 * *": [
			"qubeart.qubeart.customizations.scheduler_jobs.emaar_sales_creation.create_and_send_emaar_monthly_sales"
		 ]
	},
# 	"all": [
# 		"qubeart.tasks.all"
# 	],
# 	"daily": [
# 		"qubeart.tasks.daily"
# 	],
# 	"hourly": [
# 		"qubeart.tasks.hourly"
# 	],
# 	"weekly": [
# 		"qubeart.tasks.weekly"
# 	],
# 	"monthly": [
# 		"qubeart.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "qubeart.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.selling.doctype.quotation.quotation.make_sales_order": "qubeart.qubeart.customizations.sales_order.sales_order.make_sales_order"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "qubeart.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["qubeart.utils.before_request"]
# after_request = ["qubeart.utils.after_request"]

# Job Events
# ----------
# before_job = ["qubeart.utils.before_job"]
# after_job = ["qubeart.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"qubeart.auth.validate"
# ]

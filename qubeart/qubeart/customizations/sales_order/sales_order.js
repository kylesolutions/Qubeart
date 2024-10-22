frappe.ui.form.on("Sales Order",{
    refresh:function(frm){
        if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Qube Job Order"), function () {
				frm.events.create_job_order(frm);
			});
		}
    },
	create_job_order(frm) {
		const dialog = new frappe.ui.Dialog({
			title: __("Creae Job Order"),
			size: "extra-large",
			fields: [
				{
					fieldname: "items",
					fieldtype: "Table",
					label: __("Items to Job Order"),
					allow_bulk_edit: false,
					cannot_add_rows: true,
					cannot_delete_rows: true,
					data: [],
					fields: [
						{
							fieldname: "item_code",
							fieldtype: "Link",
							label: __("Item Code"),
							options: "Item",
							reqd: 1,
							read_only: 1,
							in_list_view: 1,
						},
						{
							fieldname: "item_name",
							fieldtype: "Data",
							label: __("Item Name"),
							read_only:1,
						},
						{
							fieldname: "qty",
							fieldtype: "Float",
							label: __("Qty"),
							reqd: 1,
							in_list_view: 1,
						},
						{
							fieldname: "uom",
							fieldtype: "options",
							options:"UOM",
							read_only:1,
							label: __("UOM"),
						},
						{
							fieldname: "description",
							fieldtype: "Text Edtitor",
							read_only:1,
							label: __("Description"),
						},
						{
							fieldname: "frame_length",
							fieldtype: "Float",
							read_only:1,
							label: __("Frame Length"),
						},
						{
							fieldname: "frame_breadth",
							fieldtype: "Float",
							read_only:1,
							label: __("Frame Breadth"),
						},
						{
							fieldname: "warehouse",
							fieldtype: "options",
							options:"Warehouse",
							read_only:1,
							label: __("Warehouse"),	
						},
						{
							fieldname: "customer_artwork",
							fieldtype: "Data",
							read_only:1,
							label: __("Customer Artwork"),	
						},
						{
							fieldname: "types_of_job",
							fieldtype: "Data",
							read_only:1,
							label: __("Types of Job"),	
						},
						{
							fieldname: "image_size",
							fieldtype: "Data",
							read_only:1,
							label: __("Image Size"),	
						},
						{
							fieldname: "border",
							fieldtype: "Data",
							read_only:1,
							label: __("Border"),	
						},
						{
							fieldname: "mirror",
							fieldtype: "Data",
							read_only:1,
							label: __("Mirror"),	
						},
						{
							fieldname: "gallery_wrap",
							fieldtype: "Data",
							read_only:1,
							label: __("Gallery Wrap"),	
						},
						{
							fieldname: "frame_code1",
							fieldtype: "Data",
							read_only:1,
							label: __("Frame Code 1"),	
						},
						{
							fieldname: "frame_code2",
							fieldtype: "Data",
							read_only:1,
							label: __("Frame Code 2"),	
						},
						{
							fieldname: "mount_code1",
							fieldtype: "Data",
							read_only:1,
							label: __("Mount Code 1"),	
						},
						{
							fieldname: "mount_code2",
							fieldtype: "Data",
							read_only:1,
							label: __("Mount Code 2"),	
						},
						{
							fieldname: "glass",
							fieldtype: "Data",
							read_only:1,
							label: __("Glass"),	
						},
						{
							fieldname: "drymount",
							fieldtype: "Data",
							read_only:1,
							label: __("DryMount"),	
						},
						{
							fieldname: "hanging_system",
							fieldtype: "Data",
							read_only:1,
							label: __("Hanging System"),	
						}

					],
				},
			],
			primary_action_label: __("Create"),
			primary_action: () => {
				var data = { items: dialog.fields_dict.items.grid.get_selected_children() };
				if (data.items && data.items.length > 0) {
					frappe.call({
						method: "qubeart.qubeart.customizations.sales_order.sales_order.job_order_creation",
						args: {
							item_details: data.items,
							notify: true,
							customer:frm.doc.customer,
							name:frm.doc.name,
							customer_name:frm.doc.customer_name,
							customer_artwork:frm.doc.custom_customer_artwork,
							types_of_job:frm.doc.custom_types_of_job,
							image_size:frm.doc.custom_image_size,
							border:frm.doc.custom_border,
							mirror:frm.doc.custom_mirror,
							gallery_wrap:frm.doc.custom_gallery_wrap_edge,
							frame_code1:frm.doc.custom_frame_code_1,
							frame_code2:frm.doc.custom_frame_code_2,
							mount_code1:frm.doc.custom_mount_code_1,
							mount_code2:frm.doc.custom_mount_code_2,
							glass:frm.doc.custom_glass,
							drymount:frm.doc.custom_drymount,
							hanging_system:frm.doc.custom_hanging_system,
						},
						freeze: true,
						freeze_message: __("Create Job Order..."),
						callback: (r) => {
							frappe.set_route("List", "Qube Job Order", { sales_order: frm.doc.name });
						},
					});
					dialog.hide();
				} else {
					frappe.msgprint(__("Please select items to job order."));
				}
			},
		});
		frm.doc.items.forEach((item) => {
			dialog.fields_dict.items.df.data.push({
				item_code: item.item_code,
				item_name:item.item_name,
				qty: item.qty,
				uom:item.uom,
				description:item.description,
				frame_length:item.custom_frame_length,
				frame_breadth:item.custom_frame_breadth,
				warehouse:item.warehouse,
				customer_artwork:item.custom_customer_artwork,
				types_of_job:item.custom_types_of_job,
				image_size:item.custom_image_size,
				border:item.custom_border,
				mirror:item.custom_mirror,
				gallery_wrap:item.custom_gallery_wrap_edge,
				frame_code1:item.custom_frame_code_1,
				frame_code2:item.custom_frame_code_2,
				mount_code1:item.custom_mount_code_1,
				mount_code2:item.custom_mount_code_2,
				glass:item.custom_glass,
				drymount:item.custom_drymount,
				hanging_system:item.custom_hanging_system,













			});
	});
		dialog.fields_dict.items.grid.refresh();
		dialog.show();
	},

})
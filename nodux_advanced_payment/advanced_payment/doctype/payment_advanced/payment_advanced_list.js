// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Payment Advanced'] = {
	add_fields: ["customer", "customer_name", "total", "status", "date", "company"],
	get_indicator: function(doc) {
		if((doc.status)=="Pending") {
			return [__("Pending"), "red", "status,=,Pending"];
		}else if ((doc.status)=="Done") {
			return [__("Done"), "green", "status,=,Done"]
		}
	},
	right_column: "total"
};

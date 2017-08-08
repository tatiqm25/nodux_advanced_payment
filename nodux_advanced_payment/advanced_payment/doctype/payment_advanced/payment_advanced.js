// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Advanced', {
	refresh: function(frm) {
		frm.disable_save();
		if (frm.doc.status== 'Pending') {
			frm.add_custom_button(__("Generar Anticipo"), function() {
				frm.events.generate_advanced(frm);
			}).addClass("btn-primary");
		}
		frm.refresh_fields();
	},

	generate_advanced: function(frm) {
		frm.save();
		frm.refresh_fields();
		frm.refresh();
		return frappe.call({
			doc: frm.doc,
			method: "generate_advanced",
			freeze: true,
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		})
		frm.refresh_fields();
		frm.refresh();
	}
});

$('#uninvoiced-start-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#uninvoiced-start',
    dateFormat: 'M d, yy'
});

$("#uninvoiced-start-vis").datepicker('setDate', new Date())


function Invoice(invoice) {
    var self = this;
    self.id = invoice.id;
    self.is_selected = ko.observable(false);
    self.number = ko.observable(invoice.number);
    self.po_number = ko.observable(invoice.po_number);
    self.total = invoice.total;
    self.created = invoice.created;
    self.sent = ko.observable(invoice.sent);
    self.member_name = invoice.member_name;
    self.email_text = ko.observable(model.invoice_email_text_default);
    self.is_unsent = ko.computed(function() {
        return !(self.sent());
    });
    self.sent_s = ko.computed(function() {
        if (self.sent()) {
            return isodate2fdate(self.sent());
        };
        return '-';
    });
};

function InvoicingViewModel() {
    // Data
    var self = this;
    self.invoice_email_text_default = null;
    self.section_active = ko.observable('');
    self.invoicing_pref_err = ko.observable(false);
    self.searching_unsent = ko.observable(true);
    self.generating = ko.observable(false);
    self.generation_failed = ko.observable(false);
    self.unsent_error = ko.observable(false);
    self.invoices = ko.observableArray([]);
    self.uninvoiced_status = ko.observable(-1); // -1: not started, 0: busy, 1: success: 2: error
    self.invoice_texts = {};
    self.invoice_ponums = {};
    self.invoices_selected = ko.computed(function() {
        return ko.utils.arrayFilter(self.invoices(), function(item) {
            return item.is_selected();
        });
    });
    self.invoices_selected_unsent = ko.computed(function() {
        return ko.utils.arrayFilter(self.invoices(), function(item) {
            return item.is_selected() && item.is_unsent();
        });
    });
    self.all_selected = ko.observable(false);
    self.select_all = function() {
        var all = self.all_selected();
        ko.utils.arrayForEach(self.invoices(), function(invoice) {
            invoice.is_selected(!all);
        });
        return true;
    };

    self.no_of_invoices = ko.computed(function() {
        return self.invoices().length;
    });
    self.no_of_unsent = ko.computed(function() {
        return ko.utils.arrayFilter(self.invoices(), function(item) {
            return item.is_unsent();
        }).length;
    });
    self.no_of_selected = ko.computed(function() { return self.invoices_selected().length; });

    // Behaviours
    self.section_active.subscribe(function(section) { 
        if (section != 'unsent') {
            $('#invoices-table').detach().appendTo('#icontainer-send');
            self.all_selected(false);
        };
    });

    self.set_invoice_conf = function(form) {
        var theform = $(form);
        var invoice_id = theform.attr('data-invoice_id');
        var email_text = theform.find('#invoice-email_text').val();
        if (email_text != self.invoice_email_text_default) { self.invoice_texts[invoice_id] = email_text; };
        $('#invoice_conf_popup').dialog('close');
    };
    self.send_selected = function() {
        var msg = "Are you sure you want to send selected " + self.no_of_selected() + " invoices? Sending invoices may take some time.";
        if (confirm(msg)) {
            send_selected();
        };
    };
    self.cancel_selected = function() {
        var msg = "Are you sure you want to cancel selected " + self.no_of_selected() + " invoices? Usages included in the invoice will be available again for invoicing. Invoices deleted can not be recovered.";
        if (confirm(msg)) {
            cancel_invoices(self.invoices_selected());
        };
    };
    self.ignore_unsent = function() {
        self.section_active('search');
        self.invoices.removeAll();
    };
    self.generate = function(form) {
        var theform = $(form);
        var params = {issuer: current_ctx};
        params['usages_before'] = theform.find("[name='usages_before']").val();
        params['only_tariff'] = theform.find("[name='only_tariff']")[0].checked;
        params['zero_usage_members'] = theform.find("[name='zero_usage_members']")[0].checked;
        jsonrpc('invoices.generate', params, on_generate, on_generate_err);
    };
};

function on_no_unsent(no_of_unsent) {
    if (!no_of_unsent && model.section_active() == 'unsent') {
        model.section_active('search');
    };
};

function on_invoice_cancel(resp) {
    var invoice_id = resp.result;
    var unsent = model.invoices();
    for (var i=0; i<unsent.length; i++) {
        var invoice = unsent[i];
        if (invoice_id == invoice.id) {
            model.invoices.remove(invoice);
        };
    };
};

function on_invoice_cancel_err(resp) {
};

function cancel_invoices(invoices) {
    for (var i=0; i<invoices.length; i++) {
        var invoice = invoices[i];
        jsonrpc('invoice.delete', {invoice_id: invoice.id}, on_invoice_cancel, on_invoice_cancel_err, true);
    };
};

function on_invoice_send(resp) {
    var invoice = resp.result;
    var invoices = model.invoices();
    for (var i=0; i<invoices.length; i++) {
        var invoice_vm = invoices[i];
        if (invoice_vm.id == invoice.id) {
            invoice_vm.sent(invoice.sent);
            invoice_vm.number(invoice.number);
            invoice_vm.is_selected(false);
        };
    };
    send_selected();
};

function on_invoice_send_err() {
};

function send_selected() {
    var selected_unsent = model.invoices_selected_unsent();
    if (selected_unsent.length) {
        var invoice = selected_unsent[0];
        var params = {invoice_id: invoice.id, po_number: invoice.po_number()};
        if (model.invoice_texts[invoice.id]) {
            params.mailtext = model.invoice_texts[invoice.id];
        };
        jsonrpc('invoice.send', params, on_invoice_send, on_invoice_send_err, true);
    };
};

model = new InvoicingViewModel();
ko.applyBindings(model);

function show_invoice(invoice) {
    $('#invoice_popup #invoice-iframe').attr('src', '/invoice/'+ invoice.id +'/html');
    $('#invoice_popup').dialog({
        title: "Invoice",
        width: 'auto'
    });
};

function show_invoice_conf(invoice) {
    var popup = $('#invoice_conf_popup');
    var form = $('#invoice_conf_popup form');
    var email_text = model.invoice_texts[invoice.id] || model.invoice_email_text_default;
    $('#invoice-email_text').val(email_text);
    form.attr('data-invoice_id', invoice.id);
    popup.dialog({
        title: "Invoice Email text",
        width: '60em'
    });
};

function on_unsent(resp) {
    model.searching_unsent(false);
    if (resp.result.length == 0) { model.section_active('search'); };
    for (var i=0; i < resp.result.length; i++) {
        var invoice = resp.result[i];
        invoice.sent = null;
        invoice.number = null;
        var invoice_vm = new Invoice(invoice);
        model.invoices.push(invoice_vm);
    };
    model.no_of_unsent.subscribe(on_no_unsent);
};

function on_unsent_error(resp) {
    model.searching_unsent(false);
    model.unsent_error(true);
};

function on_generate(resp) {
    model.generating(false);
    for (var i=0; i < resp.result.length; i++) {
        var invoice = new Invoice(resp.result[i]);
        model.invoices.push(invoice);
    };
    model.section_active('send');
};

function on_generate_err() {
    model.generation_failed(true);
};

function req_unsent() {
    jsonrpc('invoices.unsent', {issuer: current_ctx}, on_unsent, on_unsent_error);
};

function init() {
    function on_email_text(resp) {
        model.invoice_email_text_default = resp.result;
        req_unsent();
    };
    function on_email_text_err(resp) {
        model.invoicing_pref_err(true);
    };
    jsonrpc('messagecust.get', {owner_id: current_ctx, name: 'invoice'}, on_email_text, on_email_text_err, true);
    model.section_active('unsent');
};

init();

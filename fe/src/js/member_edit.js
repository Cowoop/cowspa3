var thismember = null;
var thismember_id = null;
var select_member_box = $('.select-member');

function on_member_profile(response) {
    thismember = response.result;
    $('.content-title').show();
    $('#content-title').text(thismember.profile.display_name);
    $('#content-subtitle').text("Membership no.: " + thismember_id);
    $('.section-title').slideDown('slow');
    $('.data-id').text(thismember_id);
    $('.data-username').text(thismember.account.username);
    $('input[name="first_name"]').val(thismember.profile.first_name);
    $('input[name="last_name"]').val(thismember.profile.last_name);
    $('input[name="short_description"]').val(thismember.profile.short_description);
    $('input[name="long_description"]').val(thismember.profile.long_description);
    $('input[name="address"]').val(thismember.contact.address);
    $('input[name="city"]').val(thismember.contact.city);
    $('input[name="email"]').val(thismember.contact.email);
    $('.data-email-link').attr('href', 'mailto:'+thismember.contact.email).text(thismember.contact.email);
    $('input[name="country"] option[value="' +thismember.contact.country+ '"]').attr('selected', 'selected');
    $('#member-info').slideDown();
};

function hide_sections() {
    $('.mp-section').hide();
};

function act_on_route(id) {
    select_member_box.hide();
    hide_sections();
    thismember_id = id;
    var params = {'member_id': id};
    jsonrpc('member.profile', params, on_member_profile, error);
};

function show_section(section) {
    hide_sections();
    $(section).slideToggle('slow');
};

function show_about() { show_section('#mp-about'); };
function show_billing() { show_section('#mp-billing'); };
function show_memberships() { show_section('#mp-memberships'); };
function show_contact() { show_section('#mp-contact'); };
function show_social() { show_section('#mp-social'); };
function show_pref() { show_section('#mp-pref'); };
function show_account() { show_section('#mp-account'); };

function setup_routing () {

    var routes = {
        '/:id': {
            '/about': show_about,
            '/billing': show_billing,
            '/memberships': show_memberships,
            '/contact': show_contact,
            '/social': show_contact,
            '/pref': show_pref,
            '/account': show_account,
            on: act_on_route
        },
    };

    Router(routes).use({ recurse: 'forward' }).init();
};

function on_result_click (data) {
    select_member_box.text("loading ...");
    thismember_id = data['attributes']['id'];
    var params = {'member_id': thismember_id};
    jsonrpc('member.profile', params, on_member_profile, error);
    select_member_box.hide();
}; 

function autocomplete() {
    $('#member-search').autoSuggest("/search/members", {
        selectedItemProp: "name",
        selectedValuesProp: "id", 
        searchObjProps: "name, email, id",
        minChars: 1,
        selectionLimit: 0, 
        startText: "Enter name or email or id",
        resultClick: on_result_click
    });
};

$('#st-about').click(show_about);
$('#st-contact').click(show_contact);
$('#st-billing').click(show_billing);
$('#st-memberships').click(show_memberships);
$('.section-title').hide();
$('button[value="cancel"]').click(hide_sections);

setup_routing();
autocomplete();

function edit_member(theform) {
    var action_status = $('#'+theform.attr('id') + ' .action-status');
    var inputs = theform.serializeArray();
    var params = {'member_id': thismember_id}
    for(var i in inputs) {
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Update is successful.").attr('class', 'status-success');
        window.location = "/"+resp['result']['language']+"/"+resp['result']['theme']+"/dashboard";
    };
    function error() {
        action_status.text("Update failed").attr('class', 'status-fail');
    };
    action_status.text("updating ...");
    jsonrpc('member.update', params, success, error);
};

$('.profile-edit-form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    edit_member(theform);
    return false;
});

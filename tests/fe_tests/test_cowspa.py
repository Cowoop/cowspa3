from windmill.authoring import WindmillTestClient
from windmill.authoring import setup_module, teardown_module

from util import logged_in_client, logout

def test_menus():
    client = logged_in_client()

    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertNode(xpath=u"//div[@id='main']/div/div[1]/div/div[1]/span")
    client.asserts.assertText(xpath=u"//div[@id='main']/div/div[1]/div/div[1]/span", validator=u'Member Search')
    client.asserts.assertText(xpath=u"//div[@id='main']/div/div[2]/h1", validator=u'Host Dashboard')
    client.asserts.assertNode(link=u'Dashboard')
    client.asserts.assertNode(link=u'My Profile')
    client.asserts.assertNode(link=u'Members')
    client.asserts.assertNode(link=u'Bookings')
    client.asserts.assertNode(link=u'Invoicing')
    client.asserts.assertNode(link=u'Resources')
    client.asserts.assertNode(link=u'Locations')
    client.asserts.assertNode(link=u'Reports')
    client.asserts.assertNode(id=u'account')
    client.asserts.assertNode(id=u'theme')
    client.asserts.assertNode(link=u'Logout')

    logout(client)

def test_profile():
    client = logged_in_client() #WindmillTestClient(__name__)

    client.waits.forPageLoad(timeout=u'20000')

    client.asserts.assertNode(link=u'My Profile')
    client.click(link=u'My Profile')
    client.asserts.assertNode(id=u'navlink-aboutme')
    client.asserts.assertNode(id=u'navlink-contact')
    client.asserts.assertNode(id=u'navlink-billingpreferences')
    client.asserts.assertNode(id=u'navlink-social')
    client.asserts.assertNode(id=u'navlink-memberships')
    client.asserts.assertNode(id=u'navlink-account')
    client.asserts.assertNode(id=u'navlink-preferences')

    logout(client)

#Need to add dependency such that if "Profile" menu itself
#is absent, no point running this test
def test_aboutme():
    client = logged_in_client()

    client.asserts.assertNode(link=u'My Profile')
    client.click(link=u'My Profile')
    client.click(id=u'navlink-aboutme')
    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertNode(id=u'edit-link')
    client.asserts.assertNode(xpath=u"//div[@id='about_view_form']/div[2]/div[1]")
    client.asserts.assertText(xpath=u"//div[@id='about_view_form']/div[2]/div[1]", validator=u'First name')
    client.asserts.assertNode(xpath=u"//div[@id='about_view_form']/div[3]/div[1]")
    client.asserts.assertText(xpath=u"//div[@id='about_view_form']/div[3]/div[1]", validator=u'Last name')
    client.asserts.assertNode(xpath=u"//div[@id='about_view_form']/div[4]/div[1]")
    client.asserts.assertText(xpath=u"//div[@id='about_view_form']/div[4]/div[1]", validator=u'Short description')
    client.asserts.assertNode(xpath=u"//div[@id='about_view_form']/div[5]/div[1]")
    client.asserts.assertText(xpath=u"//div[@id='about_view_form']/div[5]/div[1]", validator=u'Long description')

    logout(client)

#Need to add dependency such that if "Profile" menu itself
#is absent, no point running this test
def test_contact():
    client = logged_in_client()

    client.asserts.assertNode(link=u'My Profile')
    client.click(link=u'My Profile')
    client.click(id=u'navlink-contact')
    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertNode(id=u'edit-link')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[2]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[2]/div[1]", validator=u'Address')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[3]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[3]/div[1]", validator=u'City')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[4]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[4]/div[1]", validator=u'Country')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[5]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[5]/div[1]", validator=u'Pincode')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[6]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[6]/div[1]", validator=u'Phone')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[7]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[7]/div[1]", validator=u'Mobile')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[8]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[8]/div[1]", validator=u'Fax')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[9]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[9]/div[1]", validator=u'Email')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[10]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[10]/div[1]", validator=u'Skype')
    client.asserts.assertNode(xpath=u"//form[@id='contact_view_form']/div[11]/div[1]")
    client.asserts.assertText(xpath=u"//form[@id='contact_view_form']/div[11]/div[1]", validator=u'Sip')

    logout(client)

def test_bookings():
    client = logged_in_client()

    client.asserts.assertNode(link=u'Bookings')
    client.click(link=u'Bookings')
    client.asserts.assertNode(xpath=u'/html/body/div[2]')
    client.asserts.assertNode(link=u'New')
    client.asserts.assertNode(link=u'My Bookings')
    client.asserts.assertNode(link=u'Calendar')
    client.asserts.assertNode(link=u'Agenda')
    client.asserts.assertNode(link=u'Events')
    client.asserts.assertNode(link=u'Export')

    logout(client)

# def test_places():
#     client = logged_in_client()

#     client.asserts.assertNode(link=u'Locations')
#     client.click(link=u'Locations')
#     client.asserts.assertNode(link=u'New')
#     client.asserts.assertNode(link=u'Tariffs')
#     client.click(xpath=u'/html/body/div[2]/nav/div[6]/div[1]/a')
#     client.asserts.assertNode(xpath=u"//div[@id='main']/div/div[2]/h1")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[1]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[2]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[3]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[4]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[5]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[6]/label")
#     client.asserts.assertNode(xpath=u"//form[@id='createbizplace_form']/div[7]/label")
#     client.asserts.assertNode(id=u'save-btn')

#     logout(client)

def test_account():
    client = logged_in_client()

    client.asserts.assertNode(link=u'My Profile')
    client.click(link=u'My Profile')
    client.asserts.assertNode(id=u'navlink-account')
    client.asserts.assertNode(id=u'account') #Direct access to Account page via top right menu
    client.click(id=u'navlink-account')
    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertNode(xpath=u"//form[@id='account_edit_form']/div[1]/label")
    client.asserts.assertNode(xpath=u"//form[@id='account_edit_form']/div[2]/label")
    client.asserts.assertNode(id=u'save-btn')

    logout(client)

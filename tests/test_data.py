import datetime

admin_user = dict(username='admin', password='x', email='admin@localhost.localdmain', first_name='Admin')
admin = None

#country code 466 for "Mali"

bizplace = dict(name='Hub Timbaktu', address='118, Lotus road', city='Timbaktu', country='466', email='info@localhost.localdomain', short_description='An awesome Coworking place at Timbaktu', booking_email='booking@localhost.localdomain', host_email='hosts@localhost.localdomain')
bizplace_id = None

plan_data = dict(name="Hub 25", short_description="Not just another plan", type="tariff", default_price=90)
plan_id = None
more_plan_data = dict(name="Plan ", short_description="Not just another plan", default_price=90)
new_tariff_data = dict(name="Hub Connect", short_description="Guest Tariff", default_price=0)

member = dict(username='kit', password='x', first_name='Kit', last_name='Walker', email='kit@localhost.localdomain', enabled=True)
member_id = None

more_member = [
    dict(username='pepa', password='secret', first_name='Peter', last_name='Parker', email='peter@localhost.localdomain'),
    dict(username='cljo', password='secret', first_name='Clark', last_name='Kent', email='peter@localhost.localdomain'),
    ]
more_member_ids = []

even_more_members = [
    dict(username='mama', password='secret', first_name='Mandrake', last_name='Magician', email='mama@localhost.localdomain'),
    dict(username='lothar', password='secret', first_name='Lothar', last_name='', email='lothar@localhost.localdomain'),
    ]

even_more_member_ids = []

member_to_register = dict(first_name='Bruce', last_name='Wayne', email='bat@localhost.localdomain')

resource_data = dict(name='GlassHouse', short_description='Room with glass walls', long_description='Situated on 3rd floor GlassHouse provide nice city view. Has capacity to accomodate 17 people.', type='Type1', enabled=True, host_only=False, default_price=10, calc_mode=1)
resource_id = None

more_resources = [dict(name='RES1', short_description='Resource 1', type='Type1', default_price=10),
    dict(name='RES2', short_description='Resource 2', type='Type2', enabled=True, host_only=True, default_price=10.10),
    dict(name='RES3', short_description='Resource 3', type='Type1', default_price=11)]
more_resource_ids = []

usage = dict(resource_name='RES1', quantity=11, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)))

more_usages = [
    dict(resource_name='RES2', quantity=12, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50))),
    dict(resource_name='RES1', quantity=14, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50))),
    dict(resource_name='RES3', quantity=13, cost=1050, tax_dict=(('VAT', 100))),
    ]

invoice_preference_data = dict(due_date=30, bcc_email="pune@cowoop.net", bank_details="Bank of India,\nPune", logo="", start_number=1500000)

taxes = dict(tax=7.5, vat=5)

pricing_id = None

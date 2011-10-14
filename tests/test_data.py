import datetime

admin_user = dict(username='admin', password='x', email='admin@localhost.localdmain', first_name='Admin')

biz = dict(name='My Coworking Biz', address='118, Lotus road', city='Timbaktu', country='Mali', email='me@example.com', short_description='Social Innovators')
biz_id = None

bizplace = dict(name='Hub Timbaktu', address='118, Lotus road', city='Timbaktu', country='Mali', email='info@example.com', short_description='An awesome Coworking place at Timbaktu')
bizplace_id = None
plan_data = dict(name="Hub 25", description="Not just another plan")

more_plan_data = dict(name="Plan ", description="Not just another plan")

default_plan_data = dict(name="Hub Connect", description="Guest Tariff")

member = dict(username='kit', password='secret', first_name='Kit', last_name='Walker', email='kit@localhost.localdomain', state=dict(enabled=True, hidden=False))
member_id = None

more_member = [
    dict(username='pepa', password='secret', first_name='Peter', last_name='Parker', email='peter@example.com'),
    dict(username='cljo', password='secret', first_name='Clark', last_name='Kent', email='peter@example.com'),
    ]
more_member_ids = []

even_more_members = [
    dict(username='mama', password='secret', first_name='Mandrake', last_name='Magician', email='mama@example.com'),
    dict(username='lothar', password='secret', first_name='Lothar', last_name='', email='lothar@example.com'),
    ]

member_to_register = dict(first_name='Bruce', last_name='Wayne', email='bat@example.com')

invoice_data = dict(member=1, usages=[1,3])

more_invoice_data = [
    dict(member=2, usages=[1]),
    dict(member=3, usages=[3])
    ]

resource_data = dict(name='GlassHouse', owner='4', short_description='Room with glass walls', long_description='Situated on 3rd floor GlassHouse provide nice city view. Has capacity to accomodate 17 people.', type='Type1', state=dict(repairs=True, host_only=False))

more_resource = [dict(name='RES1', owner='4', short_description='Resource 1', type='Type1'),
    dict(name='RES2', owner='4', short_description='Resource 2', type='Type2', state=dict(enabled=True, host_only=True)),
    dict(name='RES3', owner='4', short_description='Resource 3', type='Type1')]

usage = dict(resource_id=1, resource_name='RES1', rate=11, quantity=11, calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0))

more_usages = [
    dict(resource_id=2, resource_name='RES2', rate=12, quantity=12, calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0)),
    dict(resource_id=1, resource_name='RES1', rate=14, quantity=14, calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0)),
    dict(resource_id=3, resource_name='RES3', rate=13, quantity=13, calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0)),
    ]

invoice_preference_data = [
    dict(email_text="See the attached pdf.\nThank you.", due_date=30, bcc_email="pune@hub.com", bank_details="Bank of India,\nPune", logo=""),
    dict(email_text="See the attached pdf.\nThank you.", terms_and_conditions="Pay within 20days", due_date=20, bcc_email="india@hub.com", bank_details="State Bank of India,\nMumbai", logo="")
    ]

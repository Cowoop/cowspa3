import datetime

biz = dict(name='My Coworking Biz', address='118, Lotus road', city='Timbaktu', country='Mali', email='me@example.com', short_description='Social Innovators')

bizplace = dict(name='Hub Timbaktu', address='118, Lotus road', city='Timbaktu', country='Mali', email='info@example.com', short_description='An awesome Coworking place at Timbaktu')

plan_data = dict(name="Hub 25", description="Not just another plan")

more_plan_data = dict(name="Plan ", description="Not just another plan")

default_plan_data = dict(name="Hub Connect", description="Guest Tariff")

member = dict(username='shon', password='secret', first_name='Shon', email='me@example.com', state=dict(enabled=True, hidden=False))

more_member = [
    dict(username='pepa', password='secret', first_name='Peter', last_name='Parker', email='peter@example.com'),
    dict(username='cljo', password='secret', first_name='Clark', last_name='Kent', email='peter@example.com'),
    ]

even_more_members = [
    dict(username='mama', password='secret', first_name='Mandrake', last_name='Magician', email='mama@example.com'),
    dict(username='lothar', password='secret', first_name='Lothar', last_name='', email='lothar@example.com'),
    ]

invoice_data = dict(member=1, usages=[1,3])

more_invoice_data = [
    dict(member=2, usages=[1]),
    dict(member=3, usages=[3])
    ]

resource_data = dict(name='GlassHouse', owner='BizPlace:1', short_description='Room with glass walls', long_description='Situated on 3rd floor GlassHouse provide nice city view. Has capacity to accomodate 17 people.', type='Type1')

more_resource = [dict(name='RES1', owner='BizPlace:1', short_description='Resource 1', type='Type1'),
    dict(name='RES2', owner='BizPlace:1', short_description='Resource 2', type='Type2'),
    dict(name='RES3', owner='BizPlace:1', short_description='Resource 3', type='Type1')]

usage = dict(resource_id=1, resource_name='RES1', calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0), member=1)

more_usages = [
    dict(resource_id=2, resource_name='RES2', calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0), member=1),
    dict(resource_id=1, resource_name='RES1', calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100), ('Service Tax', 50)), start_time=datetime.datetime(2011,11,01,12,0,0), member=1),
    dict(resource_id=3, resource_name='RES3', calculated_cost=1000, cost=1050, tax_dict=(('VAT', 100)), start_time=datetime.datetime(2011,11,01,12,0,0), end_time=datetime.datetime(2011,11,01,18,0,0), member=1),
    ]

role_data = dict(context = 'BizPlace:1', roles = ['director', 'host'], user_id = 1)

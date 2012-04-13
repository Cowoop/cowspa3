import commontest
import test_data

import be.apis.billingpref as billingpreflib
import be.apis.member as memberlib

def test_set_custom_billing():
    billto_member_id, billing_member_id = test_data.even_more_member_ids
    billing_member_details = memberlib.member_resource.details(billing_member_id)
    mode = 1 # Custom billing
    data = dict(name='Mandrake magic academy', address='Somewhere', city='Somecity')
    billingpreflib.billingpref_resource.update(billing_member_id, mode=mode, details=data)
    details = billingpreflib.billingpref_resource.get_details(billing_member_id)
    for attr in ('name', 'address', 'city'):
        assert data[attr] == details[attr]
    assert billingpreflib.billingpref_resource.info(billing_member_id)['mode'] == 1
    env.context.pgcursor.connection.commit()

def test_set_billto():
    pass


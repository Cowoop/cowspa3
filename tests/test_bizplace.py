import commontest
import test_data

import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.member as memberlib
import be.apis.user as userlib
import be.repository.access as dbaccess

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def test_add_bizplace():
    bizplace_id = bizplacelib.bizplace_collection.new(**test_data.bizplace)
    env.context.pgcursor.connection.commit()
    test_data.bizplace_id = bizplace_id
    assert dbaccess.OidGenerator.get_otype(bizplace_id) == "BizPlace"
    test_data.bizplace_id = bizplace_id
    default_tariff = bizplacelib.bizplace_resource.get(test_data.bizplace_id, 'default_tariff')
    test_data.default_tariff_id = default_tariff
    assert bool(int(test_data.default_tariff_id))

def test_bizplace_info():
    d = bizplacelib.bizplace_resource.info(test_data.bizplace_id)
    assert (d['short_description'], d['email']) == (test_data.bizplace['short_description'], test_data.bizplace['email'])

def test_bizplace_update():
    taxes = (('VAT', 19), ('Service Tax', 10.5))
    bizplacelib.bizplace_resource.update(test_data.bizplace_id, default_taxes=taxes)
    assert bizplacelib.bizplace_resource.get(test_data.bizplace_id, 'default_taxes') == taxes

def test_list_bizplaces_list():
    d = bizplacelib.bizplace_resource.info(test_data.bizplace_id)
    l = bizplacelib.bizplace_collection.all()
    assert d in l

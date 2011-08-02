import commontest
import test_data

import be.apis.biz as bizlib
import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.member as memberlib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_add_biz():
    biz_id = bizlib.biz_collection.new(**test_data.biz)
    env.context.pgcursor.connection.commit()
    assert biz_id == 1

def test_add_bizplace():
    test_data.bizplace['biz_id'] = 1
    bizplace_id = bizplacelib.bizplace_collection.new(**test_data.bizplace)
    env.context.pgcursor.connection.commit()
    test_data.bizplace_id = bizplace_id
    assert bizplace_id == 1

def test_biz_info():
    d = bizlib.biz_resource.info(1)
    assert (d['short_description'], d['email']) == (test_data.biz['short_description'], test_data.biz['email'])

def test_bizplace_info():
    d = bizplacelib.bizplace_resource.info(1)
    assert (d['short_description'], d['email']) == (test_data.bizplace['short_description'], test_data.bizplace['email'])

def test_bizplace_update():
    taxes = (('VAT', 19), ('Service Tax', 10.5))
    bizplacelib.bizplace_resource.update(1, taxes=taxes)
    assert bizplacelib.bizplace_resource.get(1, 'taxes') == taxes

def test_list_bizplaces_list():
    d = bizplacelib.bizplace_resource.info(1)
    l = bizplacelib.bizplace_collection .list()
    assert d in l

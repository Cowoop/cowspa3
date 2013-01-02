import commontest
import test_data

import be.apis.bizplace as bizplacelib
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
    city = 'Pune'
    bizplacelib.bizplace_resource.update(test_data.bizplace_id, city=city)
    assert bizplacelib.bizplace_resource.get(test_data.bizplace_id, 'city') == city

def test_list_bizplaces_list():
    d = bizplacelib.bizplace_resource.info(test_data.bizplace_id)
    l = bizplacelib.bizplace_collection.all()
    assert d in l

def test_add_bizplace_with_sample():
    bizplace_id = bizplacelib.bizplace_collection.new(**test_data.bizplace_sample)
    env.context.pgcursor.connection.commit()
    assert dbaccess.OidGenerator.get_otype(bizplace_id) == "BizPlace"
    default_tariff = bizplacelib.bizplace_resource.get(bizplace_id, 'default_tariff')
    assert bool(int(test_data.default_tariff_id))

def test_search_member():
    bizplace_id = test_data.bizplace_id
    data = test_data.bizplace_member
    data['bizplace_id'] = bizplace_id
    member_id = memberlib.member_collection.new(**data)
    test_data.membership_member_id = member_id
    env.context.pgcursor.connection.commit()
    assert isinstance(member_id, (int, long)) == True
    term = test_data.bizplace_member['first_name'][:2]
    term += ' '
    term += test_data.bizplace_member['last_name'][:2]
    result = memberlib.member_collection.search(term, bizplace_id)
    assert member_id == result[0]['id'] # assumption Hulk is at 0th place

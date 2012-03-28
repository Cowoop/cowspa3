import commontest
import test_data
import be.repository.access as dbaccess
import be.apis.member as memberlib
import be.apis.user as userlib
from nose.tools import nottest

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def test_create_member(data=None):
    data = data if data else test_data.member
    member_id = memberlib.member_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert isinstance(member_id, (int, long)) == True
    test_data.member_id = member_id
    return member_id

def test_member_object():
    m = dbaccess.member_store.get(test_data.member_id)
    assert m.first_name == test_data.member['first_name']
    m.first_name = 'Kit'
    assert m.first_name == 'Kit'
    m.update(first_name='Kit', last_name='Walker')
    assert m.first_name, m.last_name == ('Kit', 'Walker')

def test_update_member():
    old_state = memberlib.member_resource.get(test_data.member_id, 'enabled')
    new_state = dict(enabled=False)
    memberlib.member_resource.update(test_data.member_id, **new_state)
    assert old_state == test_data.member['enabled']
    assert new_state['enabled'] == memberlib.member_resource.get(test_data.member_id, 'enabled')

def test_contact_update():
    mod_data = dict(address='Address line 1\nAddress line 2', city='Timbaktu', province='Test State', country='Mail', pincode='012345')
    memberlib.member_resource.update(test_data.member_id, **mod_data)
    details = memberlib.member_resource.details(test_data.member_id)
    for attr in mod_data.keys():
        assert details['contact'][attr] == mod_data[attr]

def test_auth():
    assert userlib.authenticate(test_data.member['username'], 'password') != True
    assert userlib.authenticate(test_data.member['username'], test_data.member['password']) == True

def test_create_more_members():
    for data in test_data.more_member:
        member_id = memberlib.member_collection.new(**data)
        test_data.more_member_ids.append(member_id)
    env.context.pgcursor.connection.commit()

@nottest
def test_create_10k_members():
    data = {}
    data.update(test_data.member)
    for i in range(10000):
        data['username'] = test_data.member['username'] + str(i)
        member_id = memberlib.member_collection.new(**data)
        env.context.pgcursor.connection.commit()

def test_info():
    m_id = test_data.member_id
    info = memberlib.member_resource.info(m_id)
    assert info.id == m_id and test_data.member['first_name'] in info.name

def test_search():
    result = memberlib.member_collection.search("pet", 0)
    assert len(result) >= 1
    result = memberlib.member_collection.search_deprecated(str(test_data.member_id))
    assert test_data.member['first_name'] in result[0]['name']
    result = memberlib.member_collection.search(test_data.member['first_name'], 0)
    #assert len(result) == 0 # user kit is not enabled
    assert len(memberlib.member_collection.search("Nobody", 0)) == 0

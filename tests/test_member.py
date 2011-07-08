import commontest
import be.apis.member as memberlib
import be.apis.user as userlib
from nose.tools import nottest

member_data = dict(username='shon', password='secret', first_name='Shon', email='me@example.com', state=1)
more_member_data = [
    dict(username='pepa', password='secret', first_name='Peter', last_name='Parker', email='peter@example.com'),
    dict(username='cljo', password='secret', first_name='Clark', last_name='Kent', email='peter@example.com'),
    ]

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_create_member(test_data=None):
    data = test_data if test_data else member_data
    print data
    member_id = memberlib.member_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert isinstance(member_id, (int, long)) == True

def test_update_member():
    old_state = memberlib.member_resource.get(1, 'state')
    new_state = 0
    mod_data = dict(state=new_state)
    memberlib.member_resource.update(1, **mod_data)
    assert old_state == member_data['state']
    #assert new_state == memberlib.member_resource.get(1, 'state')

def test_auth():
    assert userlib.authenticate(member_data['username'], 'password') != True
    assert userlib.authenticate(member_data['username'], member_data['password']) == True

def test_create_more_members():
    for data in more_member_data:
        test_create_member(data)

@nottest
def test_create_10k_members():
    data = {}
    data.update(member_data)
    for i in range(10000):
        data['username'] = member_data['username'] + str(i)
        test_create_member(data)
        env.context.pgcursor.connection.commit()
test_create_10k_members.disabled = True

def test_info():
    m_id = 1
    info = memberlib.member_resource.info(m_id)
    assert info.id == m_id and member_data['first_name'] in info.display_name


import commontest
import be.apis.member as memberlib

test_member_data = dict(username='shon', password='secret', first_name='Shon', email='me@example.com')

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_create_member(test_data=None):
    data = test_data if test_data else test_member_data
    member_id = memberlib.new(**data)
    env.context.pgcursor.connection.commit()
    assert isinstance(member_id, int) == True

def test_create_10k_members():
    data = {}
    data.update(test_member_data)
    for i in range(10000):
        data['username'] = test_member_data['username'] + str(i)
        test_create_member(data)
        env.context.pgcursor.connection.commit()

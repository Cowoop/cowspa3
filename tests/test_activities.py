import commontest
import test_data
import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.user as userlib

member_data = dict(name='Shon', location='India', id=1, actor_name='test-system', actor_id=100)
member_data2 = dict(name='gaurav', location='India', id=2, actor_name='test-system', actor_id=100)
cur_time = datetime.datetime.now()
member_updt_data = dict(name=member_data['name'], id=member_data['id'], attrs='state', actor_name='test-system', actor_id=100)

def setup():
    commontest.setup_test_env()
    token = userlib.login(test_data.member['username'], test_data.member['password'])
    userlib.set_context(token)
    env.context.pgcursor.connection.commit()

def teardown():
    activitylib.delete([1, 2, 3])
    messages = activitylib.find_activities_by_categories(['MemberManagement'], cur_time, datetime.datetime.now())
    assert len(messages) == 0
    env.context.pgcursor.connection.commit()

def test_create_activities():
    activity_id = activitylib.add('member_management', 'member_created', member_data, datetime.datetime.now())

    activity_id = activitylib.add('member_management', 'member_updated', member_updt_data, datetime.datetime.now())

    activity_ctx = ['BizPlace:3', dbaccess.stores.member_store.ref(member_data2['id'])]
    activity_id = activitylib.add('member_management','member_created', member_data2, datetime.datetime.now())
    env.context.pgcursor.connection.commit()

def test_find_latest():
    msgs = activitylib.get_latest()
    assert msgs[0] == 'New member Shon created by shon.'

def test_find_activities_by_categories():

    messages = activitylib.find_activities_by_categories(['member_management'], cur_time, datetime.datetime.now())
    #for msg in messages: print msg
    activities = dbaccess.list_activities_by_categories(['member_management'],cur_time,datetime.datetime.now())
    assert len(activities) == 3
    activity = activities[1]
    assert activity['category'] == 'member_management'
    assert activity['name'] == 'member_updated'
    assert activity['data']['id'] == 1
    assert activity['data']['attrs'] == 'state'


def test_find_activities_by_names():

    messages = activitylib.find_activities_by_names(['member_created'], cur_time, datetime.datetime.now())
    #for msg in messages: print msg
    activities = dbaccess.list_activities_by_names(['member_created'], cur_time, datetime.datetime.now())
    activity = activities[1]
    assert activity['category'] == 'member_management'
    assert activity['name'] == 'member_created'
    assert activity['data']['name'] == member_data['name']

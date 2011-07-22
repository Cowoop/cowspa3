import commontest
import datetime
import pickle
import be.repository.access as dbaccess
import be.apis.member as memberlib
import be.apis.activities as activitylib
import be.apis.user as userlib
from nose.tools import nottest

member_data = dict(username='shon', password='secret', first_name='Shon', email='me@example.com', state=dict(enabled=True, hidden=False))
member_data2 = dict(username='gaurav', password='secret', first_name='Gaurav', email='me@example.com', state=dict(enabled=False, hidden=False))
cur_time = datetime.datetime.now()

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_activity_new_member(test_data=None):

    data = test_data if test_data else member_data
    member_id = memberlib.member_collection.new(**data)
    env.context.pgcursor.connection.commit()
    
    messages = activitylib.activity_collection.find_activities_by_categories(['MemberManagement'], cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activity = dbaccess.Activity()
    activities = activity.list_by_categories(['MemberManagement'], cur_time, datetime.datetime.now())
    activity = activities[0]
    assert activity['category'] == 'MemberManagement'
    assert pickle.loads(activity['data'])['name'] == data['first_name']
    
    data = test_data if test_data else member_data2
    member_id = memberlib.member_collection.new(**data)
    env.context.pgcursor.connection.commit()
    
    messages = activitylib.activity_collection.find_activities_by_name('MemberCreated', cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activity = dbaccess.Activity()
    activities = activity.list_by_name('MemberCreated', cur_time, datetime.datetime.now())
    activity = activities[1]
    assert activity['category'] == 'MemberManagement'
    assert activity['name'] == 'MemberCreated'
    assert pickle.loads(activity['data'])['name'] == data['first_name']
                       

def test_activity_update_member():

    new_state = dict(enabled=False, hidden=True)
    mod_data = dict(state=new_state)
    memberlib.member_resource.update(1, **mod_data)
    
    messages = activitylib.activity_collection.find_activities_by_categories(['MemberManagement'], cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activity = dbaccess.Activity()
    activities = activity.list_by_categories(['MemberManagement'],cur_time,datetime.datetime.now())
    activity = activities[2]
    assert activity['category'] == 'MemberManagement'
    assert activity['name'] == 'MemberUpdated'
    assert pickle.loads(activity['data'])['user_id'] == 1
    assert pickle.loads(activity['data'])['attrs'] == 'state'
    
    new_email = 'gaurav@mymail.com'
    new_state = dict(enabled=True, hidden=True)
    mod_data = dict(email=new_email, state=new_state)
    memberlib.member_resource.update(2, **mod_data)
    
    messages = activitylib.activity_collection.find_activities_by_name('MemberUpdated', cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activity = dbaccess.Activity()
    activities = activity.list_by_name('MemberUpdated',cur_time,datetime.datetime.now())
    activity = activities[1]
    assert activity['category'] == 'MemberManagement'
    assert pickle.loads(activity['data'])['user_id'] == 2
    print pickle.loads(activity['data'])['attrs']
    assert len(pickle.loads(activity['data'])['attrs'].split(', ')) == 2

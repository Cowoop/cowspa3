import commontest
import datetime
import cPickle
import be.repository.access as dbaccess
import be.apis.activities as activitylib

member_data = dict(name='Shon', location='India', user_id=1)
member_data2 = dict(name='gaurav', location='India', user_id=2)
cur_time = datetime.datetime.now()

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_find_activities_by_categories():

    activity_id = activitylib.add('MemberManagement', 'MemberCreated', 1, member_data, datetime.datetime.now())
    env.context.pgcursor.connection.commit()
    
    data = dict(user_id=1, attrs='state')
    activity_id = activitylib.add('MemberManagement', 'MemberUpdated', 1, data, datetime.datetime.now())
    
    messages = activitylib.find_activities_by_categories(['MemberManagement'], cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activities = dbaccess.list_activities_by_categories(['MemberManagement'],cur_time,datetime.datetime.now())
    assert len(activities) == 2
    activity = activities[1]
    assert activity['category'] == 'MemberManagement'
    assert activity['name'] == 'MemberUpdated'
    assert cPickle.loads(str(activity['data']))['user_id'] == 1
    assert cPickle.loads(str(activity['data']))['attrs'] == 'state'

                       
def test_find_activities_by_name():

    activity_id = activitylib.add('MemberManagement', 'MemberCreated', 2, member_data2, datetime.datetime.now())
    env.context.pgcursor.connection.commit()
    
    messages = activitylib.find_activities_by_name('MemberCreated', cur_time, datetime.datetime.now())
    #for msg in messages:
    #    print msg
        
    activities = dbaccess.list_activities_by_name('MemberCreated', cur_time, datetime.datetime.now())
    activity = activities[1]
    assert activity['category'] == 'MemberManagement'
    assert activity['name'] == 'MemberCreated'
    assert cPickle.loads(str(activity['data']))['name'] == member_data2['name'] 

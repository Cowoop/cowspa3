import commontest
import test_data

import datetime
import be.repository.access as dbaccess
import be.apis.usage as usagelib
import test_resources

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_add_usage():
    data = test_data.usage
    data['member'] = test_data.member_id
    data['resource_id'] = test_data.resource_id
    data['start_time'] = datetime.datetime.now().isoformat()
    data['end_time'] = datetime.datetime.now().isoformat()
    data['created_by'] = test_data.admin
    data['invoice'] = 1
    test_data.usage_id = usagelib.usage_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert isinstance(test_data.usage_id, (int, long))

def test_update_usage():
    old_cost = usagelib.usage_resource.get(test_data.usage_id, 'cost')
    new_cost = 2000
    mod_data = dict(cost=new_cost)
    usagelib.usage_resource.update(test_data.usage_id, **mod_data)
    assert old_cost == test_data.usage['cost']
    assert new_cost == usagelib.usage_resource.info(test_data.usage_id)['cost']

def test_delete_or_cancel_usage(): 
    usage_id = usagelib.usage_collection.delete(test_data.usage_id, test_data.admin)
    assert usagelib.usage_resource.get(usage_id, 'cancelled_against') == test_data.usage_id
    assert usagelib.usage_resource.get(usage_id, 'cost') == -usagelib.usage_resource.get(test_data.usage_id, 'cost')    
    assert usagelib.usage_collection.delete(usage_id, test_data.admin) == True
    
def test_add_more_usage():
    for data in test_data.more_usages:
        data['member'] = test_data.member_id
        data['resource_id'] = test_data.resource_id
        data['start_time'] = datetime.datetime.now().isoformat()
        data['end_time'] = datetime.datetime.now().isoformat()
        data['created_by'] = test_data.admin
        usage_id = usagelib.usage_collection.new(**data)
    env.context.pgcursor.connection.commit()

def test_find_by():
    data = dict(start=(datetime.datetime.now() - datetime.timedelta(1)), end=datetime.datetime.now())
    usages = usagelib.usage_collection.find(**data)
    assert len(usages) >= 4
    for usage in usages:
        assert usage['start_time'] >= data['start'] and usage['start_time'] <= data['end']

    data = dict(res_owner_ids=[test_data.bizplace_id])
    usages = usagelib.usage_collection.find(**data)
    assert bool(usages)

def test_delete_usage():
    ret = usagelib.usage_collection._delete(1)
    assert ret == True


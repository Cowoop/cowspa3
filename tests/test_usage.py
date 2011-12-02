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

def test_add_more_usage():
    for data in test_data.more_usages:
        data['member'] = test_data.member_id
        data['resource_id'] = test_data.resource_id
        data['start_time'] = datetime.datetime.now().isoformat()
        data['end_time'] = datetime.datetime.now().isoformat()
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
    ret = usagelib.usage_collection.delete(1)
    assert ret == True


import commontest
import test_data

import datetime
import be.repository.access as dbaccess
import be.apis.usage as usagelib
import test_resources

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_add_usage():
    usage_id = usagelib.usage_collection.add(**test_data.usage)
    env.context.pgcursor.connection.commit()
    assert usage_id == 1

def test_update_usage():
    old_cost = usagelib.usage_resource.get(1,'cost')
    new_cost = 2000
    mod_data = dict(cost=new_cost)
    usagelib.usage_resource.update(1, mod_data)
    assert old_cost == test_data.usage['cost']
    assert new_cost == usagelib.usage_resource.info(1)['cost']

def test_add_more_usage():
    for data in test_data.more_usages:
        usage_id = usagelib.usage_collection.add(**data)
    env.context.pgcursor.connection.commit()

def test_find_by():
    data = dict(start=datetime.datetime(2011,11,01,0,0,0), end=datetime.datetime(2011,12,01,0,0,0))
    usages = usagelib.usage_resource.find(**data)
    assert len(usages) == 4
    for usage in usages:
        assert usage['start_time'] >= data['start'] and usage['start_time'] <= data['end']

    data = dict(start=datetime.datetime(2011,12,01,0,0,0), resource_ids=[2,3])
    usages = usagelib.usage_resource.find(**data)
    assert len(usages) == 0
    
    data = dict(resource_ids=[2], res_owner_refs=['BizPlace:1'])
    usages = usagelib.usage_resource.find(**data)
    assert len(usages) == 1
    assert usages[0]['resource_id'] in [2] 
    
    data = dict(start=datetime.datetime(2011,11,01,0,0,0), resource_types=['Type1'])
    usages = usagelib.usage_resource.find(**data)
    for usage in usages:
        assert usage['start_time'] >= data['start'] and usage['resource_id'] in [1, 2, 4]
    
def test_delete_usage():
    ret = usagelib.usage_collection.delete(1)
    assert ret == True


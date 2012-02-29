import commontest
import test_data

import be.apis.resource as resourcelib
import commonlib.shared.constants as constants

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def test_create():
    resource_data = test_data.resource_data
    resource_data['owner'] = test_data.bizplace_id
    res_id = resourcelib.resource_collection.new(**resource_data)
    env.context.pgcursor.connection.commit()
    test_data.resource_id = res_id
    assert isinstance(res_id, (int, long))

def test_create_more():
    for data in test_data.more_resources:
        data['owner'] = test_data.bizplace_id
        res_id = resourcelib.resource_collection.new(**data)
        test_data.more_resource_ids.append(res_id)
    env.context.pgcursor.connection.commit()
    assert res_id != 1

def test_info():
    info = resourcelib.resource_resource.info(test_data.resource_id)
    assert info.name == test_data.resource_data['name']
    assert info.calc_mode == test_data.resource_data['calc_mode']
    assert len(resourcelib.resource_collection.list(test_data.bizplace_id)) >= 4

def test_update():
    new_name = 'GlassHouse II'
    resourcelib.resource_resource.update(test_data.resource_id, name=new_name)
    env.context.pgcursor.connection.commit()
    assert resourcelib.resource_resource.get(test_data.resource_id, 'name') == new_name

def test_set_relations():
    res_ids = test_data.more_resource_ids
    relations = [(True, res_ids[0]), (True, res_ids[1]), (False, res_ids[2])]
    resourcelib.resource_resource.set_relations(test_data.resource_id, relations)
    env.context.pgcursor.connection.commit()
    relation_dicts = resourcelib.resource_resource.get_relations(test_data.resource_id)
    assert relation_dicts[False] == [dict(id=res_ids[2], name='RES3', calc_mode=2)]
    assert relation_dicts[True] == [dict(id=res_ids[0], name='RES1', calc_mode=2), dict(id=res_ids[1], name='RES2', calc_mode=2)]
    assert res_ids[2] not in resourcelib.resource_collection.bookable(test_data.bizplace_id)

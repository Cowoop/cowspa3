import commontest
import test_data

import be.apis.resource as resourcelib
import commonlib.shared.constants as constants

rr = constants.resource_relations

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_create():
    res_id = resourcelib.resource_collection.new(**test_data.resource_data)
    env.context.pgcursor.connection.commit()
    assert res_id == 1

def test_create_more():
    for data in test_data.more_resource:
        res_id = resourcelib.resource_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert res_id != 1

def test_info():
    assert resourcelib.resource_resource.info(1).name == test_data.resource_data['name']

def test_update():
    new_name = 'GlassHouse II'
    resourcelib.resource_resource.update(1, name=new_name)
    env.context.pgcursor.connection.commit()
    assert resourcelib.resource_resource.get(1, 'name') == new_name

def test_set_relations():
    relations = [('contains', 2), ('contains', 3), ('suggests', 4)]
    resourcelib.resource_resource.set_relations(1, relations)
    env.context.pgcursor.connection.commit()
    relation_dicts = resourcelib.resource_resource.get_relations(1)
    assert relation_dicts['suggests'] == [dict(id=4, name='RES3')]
    assert relation_dicts['contains'] == [dict(id=2, name='RES1'), dict(id=3, name='RES2')]

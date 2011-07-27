import commontest
import test_plans
import be.apis.resource as resourcelib
import commonlib.shared.constants as constants

rr = constants.resource_relations

resource_data = dict(name='GlassHouse', owner='BizPlace:1', short_description='Room with glass walls', long_description='Situated on 3rd floor GlassHouse provide nice city view. Has capacity to accomodate 17 people.', type='Type1')
more_resource_data = [dict(name='RES1', owner='BizPlace:1', short_description='Resource 1', type='Type1'),
    dict(name='RES2', owner='BizPlace:1', short_description='Resource 2', type='Type2'),
    dict(name='RES3', owner='BizPlace:1', short_description='Resource 3', type='Type1')]

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    test_plans.test_add_bizplace()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_create():
    res_id = resourcelib.resource_collection.new(**resource_data)
    env.context.pgcursor.connection.commit()
    assert res_id == 1

def test_create_more():
    for data in more_resource_data:
        res_id = resourcelib.resource_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert res_id != 1

def test_info():
    assert resourcelib.resource_resource.info(1).name == resource_data['name']

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

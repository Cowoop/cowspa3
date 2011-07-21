import commontest
import test_plans
import be.apis.resource as resourcelib

resource_data = dict(name='GlassHouse', owner='BizPlace:1', short_description='Room with glass walls', long_description='Situated on 3rd floor GlassHouse provide nice city view. Has capacity to accomodate 17 people.')

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
    print(res_id)
    assert res_id == 1

def test_info():
    print(resourcelib.resource_resource.info(1))

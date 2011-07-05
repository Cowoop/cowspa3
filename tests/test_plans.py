import commontest
import test_member
import be.apis.biz as bizlib
import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.member as memberlib

biz_data = dict(name='My Coworking Biz', address='118, Lotus road', city='Timbaktu', country='Mali', email='me@example.com', short_description='Social Innovators')
bizplace_data = dict(name='Hub Timbaktu', address='118, Lotus road', city='Timbaktu', country='Mali', email='info@example.com', short_description='An awesome Coworking place at Timbaktu')
plan_data = dict(name="Hub 25", description="Not just another plan")

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def teardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_add_biz():
    biz_ob = bizlib.biz_collection
    #print biz_data['name']
    biz_id = biz_ob.new(**biz_data)
    env.context.pgcursor.connection.commit()
    print "sdfg"+str(biz_id)
    assert biz_id == 1

def test_add_bizplace():
    bizplace_data['biz_id'] = 1
    bizplace_id = bizplacelib.new(**bizplace_data)
    env.context.pgcursor.connection.commit()
    assert bizplace_id == 1

def test_biz_info():
    biz_ob = bizlib.biz_resource
    d = biz_ob.info(1)
    assert (d['short_description'], d['email']) == (biz_data['short_description'], biz_data['email'])

def test_bizplace_info():
    d = bizplacelib.info(1)
    assert (d['short_description'], d['email']) == (bizplace_data['short_description'], bizplace_data['email'])

def test_list_bizplaces_list():
    d = bizplacelib.info(1)
    l = bizplacelib.list()
    assert d in l

def test_add_plan():
    plan_data['bizplace_id'] = 1
    plan_ob = planlib.plan_collection
    plan_id = plan_ob.new(**plan_data)
    env.context.pgcursor.connection.commit()
    assert plan_id == 1

def test_add_subscribers():
    test_member.test_create_member()
    test_member.test_create_more_members()
    plan_ob = planlib.plan_resource
    plan_ob.new_subscribers(1, [1, 2, 3])
    env.context.pgcursor.connection.commit()

def test_subscribers():
    plan_ob = planlib.plan_resource
    subscribers = plan_ob.subscribers(1)
    assert len(subscribers) == 3

def test_plan_info():
    plan_ob = planlib.plan_resource
    plan_ob.info(1)

def test_list_members():
    member_ob = memberlib.member_collection
    assert len(member_ob.list(1, [1])) == 3


#dbaccess.find_members_in_member_bizplaces(1)
#dbaccess.add_membership(1, 2)

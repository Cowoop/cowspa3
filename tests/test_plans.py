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

def xteardown():
    commontest.destroy_test_env()
    env.context.pgcursor.connection.commit()

def test_add_biz():
    biz_id = bizlib.new(**biz_data)
    env.context.pgcursor.connection.commit()
    assert biz_id == 1

def test_add_bizplace():
    bizplace_data['biz_id'] = 1
    bizplace_id = bizplacelib.new(**bizplace_data)
    env.context.pgcursor.connection.commit()
    assert bizplace_id == 1

def test_add_plan():
    plan_data['bizplace_id'] = 1
    plan_id = planlib.new(**plan_data)
    env.context.pgcursor.connection.commit()
    assert plan_id == 1

def test_add_subscribers():
    test_member.test_create_member()
    test_member.test_create_more_members()
    planlib.new_subscribers(1, [1, 2, 3])
    env.context.pgcursor.connection.commit()

def test_list_members():
    print(memberlib.list(1, [1]))

#dbaccess.find_members_in_member_bizplaces(1)
#dbaccess.add_membership(1, 2)

import datetime
import commontest
import test_data

import test_member
import be.apis.biz as bizlib
import be.apis.bizplace as bizplacelib
import be.apis.plan as planlib
import be.apis.member as memberlib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_add_plan():
    test_data.plan_data['bizplace_id'] = 1
    plan_id = planlib.plan_collection.new(**test_data.plan_data)
    env.context.pgcursor.connection.commit()
    assert plan_id == 1

def test_add_subscribers():
    starts = datetime.datetime(2011, 1, 1, 0, 0, 1)
    planlib.plan_resource.new_subscribers(1, starts, [1, 2, 3])
    env.context.pgcursor.connection.commit()

def test_find_bizplace_plans():
    data = {}
    data.update(test_data.more_plan_data)
    for i in range(4):
        data['name'] = test_data.more_plan_data['name'] + str(i)
        data['bizplace_id'] = 1
        planlib.plan_collection.new(**data)
        env.context.pgcursor.connection.commit()
    plans = bizplacelib.bizplace_resource.plans(1)
    assert len(plans) == 5

def test_subscribers():
    subscribers = planlib.plan_resource.subscribers(1)
    assert len(subscribers) == 3

def test_plan_info():
    planlib.plan_resource.info(1)

#dbaccess.find_members_in_member_bizplaces(1)
#dbaccess.add_membership(1, 2)

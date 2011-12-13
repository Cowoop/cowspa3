import datetime
import commontest
import test_data

import test_member
import be.apis.bizplace as bizplacelib
import be.apis.resource as planlib
import be.apis.membership as membershiplib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def test_add_plan():
    test_data.plan_data['owner'] = test_data.bizplace_id
    plan_id = planlib.resource_collection.new(**test_data.plan_data)
    env.context.pgcursor.connection.commit()
    test_data.plan_id = plan_id
    assert str(plan_id).isdigit() == True

def test_add_members():
    starts = datetime.date(2011, 1, 1).isoformat()
    ends = datetime.date(2011, 3, 5).isoformat()
    membershiplib.memberships.bulk_new(test_data.plan_id, test_data.more_member_ids, starts, ends)
    env.context.pgcursor.connection.commit()

def test_find_bizplace_plans():
    data = {}
    data.update(test_data.more_plan_data)
    for i in range(4):
        data['name'] = test_data.more_plan_data['name'] + str(i)
        data['owner'] = test_data.bizplace_id
        planlib.resource_collection.new_tariff(**data)
        env.context.pgcursor.connection.commit()
    plans = bizplacelib.bizplace_resource.plans(test_data.bizplace_id)
    assert len(plans) >= 5

def test_members():
    members = membershiplib.memberships.list(by_tariff=test_data.plan_id, at_time=datetime.date(2011, 1, 15).isoformat())
    assert len(members) == len(test_data.more_member_ids)

def test_plan_info():
    planlib.resource_resource.info(test_data.plan_id)

#dbaccess.find_members_in_member_bizplaces(1)
#dbaccess.add_membership(1, 2)

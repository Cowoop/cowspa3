import datetime
from nose.tools import assert_raises
import commontest
import test_data

import be.apis.bizplace as bizplacelib
import be.apis.resource as resourcelib
import be.apis.pricing as pricinglib
import be.apis.membership as membershiplib
import be.errors
import be.repository.access as dbaccess
import test_member

# dependencies bizplace plan resource

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    commontest.setup_system_context()

def _add_plan(data):
    plan_id = resourcelib.resource_collection.new_tariff(**data)
    env.context.pgcursor.connection.commit()
    return plan_id

def test_add_new_tariff():
    plan_data = test_data.new_tariff_data
    plan_data['owner'] = test_data.bizplace_id
    plan_id =_add_plan(plan_data)
    test_data.new_tariff_id = plan_id
    assert test_data.plan_id != plan_id

def test_add_pricing_for_a_plan():
    amount = 20
    starts = datetime.date(2011,8,1).isoformat() # this starts is ignored
    pricing_id  = pricinglib.pricings.new(test_data.resource_id, test_data.plan_id, starts, amount)
    info = pricinglib.pricing.info(pricing_id)
    env.context.pgcursor.connection.commit()
    assert info.resource == test_data.resource_id and isinstance(pricing_id, (int, long))

def test_add_pricing_for_a_plan_with_same_date():
    amount = 20
    test_data.price_w_plan = amount
    starts = datetime.date(2011,8,1).isoformat()
    try:
        pricing_id  = pricinglib.pricings.new(test_data.resource_id, test_data.plan_id, starts, amount) # adding this pricing must work not next
    except Exception, err:
        assert True#isinstance(err, be.errors.ErrorWithHint)
    else:
        assert False 

def test_add_pricing_for_default_tariff():
    amount = 50
    test_data.price_wo_plan = amount
    starts = datetime.date(2011,8,1).isoformat()
    pricing_id = pricinglib.pricings.new(test_data.resource_id, test_data.default_tariff_id, starts, amount)
    info = pricinglib.pricing.info(pricing_id)
    test_data.default_pricing_id = pricing_id
    env.context.pgcursor.connection.commit()
    assert info.amount == amount

def test_add_member_w_plan_subscription():
    data = test_data.even_more_members[0]
    member_id = test_member.test_create_member(data)
    starts = datetime.date.today().isoformat()
    ends = (datetime.date.today()+datetime.timedelta(30)).isoformat()
    created_by = test_data.admin
    assert membershiplib.memberships.new(test_data.plan_id, member_id, starts, ends) == True
    test_data.member_w_plan = member_id
    env.context.pgcursor.connection.commit()

def test_member_tariff():
    return pricinglib.member_tariff(test_data.member_w_plan, test_data.bizplace_id)

def test_add_member_wo_plan_subscription():
    data = test_data.even_more_members[1]
    member_id = test_member.test_create_member(data)
    test_data.member_wo_plan = member_id
    env.context.pgcursor.connection.commit()

def test_get_pricing_for_member_w_plan():
    usage_time = datetime.datetime.now()
    assert pricinglib.pricings.get(test_data.member_w_plan, test_data.resource_id, usage_time) == test_data.price_w_plan

def test_get_pricing_for_member_wo_plan():
    usage_time = datetime.datetime.now()
    assert pricinglib.get(test_data.member_wo_plan, test_data.resource_id, usage_time) == test_data.price_wo_plan

def test_cost():
    quantity = 10
    starts = datetime.datetime.now().isoformat()
    ends = (datetime.datetime.now() + datetime.timedelta(0, 10*3600)).isoformat()
    cost = pricinglib.calculate_cost(test_data.member_w_plan, test_data.resource_id, quantity, starts, ends)
    rate = pricinglib.pricings.get(test_data.member_w_plan, test_data.resource_id, starts)
    assert cost == (quantity * rate)

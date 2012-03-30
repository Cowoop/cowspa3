import datetime
from nose.tools import assert_raises
import commontest
import test_data

import be.apis.bizplace as bizplacelib
import be.libs.cost as costlib
import be.apis.resource as resourcelib
import be.apis.pricing as pricinglib
import be.apis.membership as membershiplib
import be.errors
import be.repository.access as dbaccess
import test_member
import be.apis.invoicepref as invoicepreflib

# dependencies bizplace plan resource

a_start_date = datetime.date(2011,8,1)
a_end_date = datetime.date(2015,8,1)
membership_starts = datetime.date(2013, 1, 2)
membership_ends = datetime.date(2013, 3, 31)
a_usage_time = datetime.datetime(2013, 1, 10, 10, 1, 1) # within membership_starts - membership_ends
another_usage_time = datetime.datetime(2013, 3, 31, 18, 0, 0) # on last day of membership

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
    starts = a_start_date.isoformat()
    ends = a_end_date.isoformat()
    pricing_id  = pricinglib.pricings.new(test_data.resource_id, test_data.plan_id, starts, amount, ends)
    test_data.pricing_id = pricing_id
    info = pricinglib.pricing.info(pricing_id)
    env.context.pgcursor.connection.commit()
    assert info.resource == test_data.resource_id and isinstance(pricing_id, (int, long))

def test_add_pricing_with_bad_end_date():
    amount = 20
    starts = a_start_date.isoformat()
    ends = (a_start_date - datetime.timedelta(7)).isoformat() # end smaller than start
    assert_raises(AssertionError, pricinglib.pricings.new, *(test_data.resource_id, test_data.plan_id, starts, amount, ends))

def test_add_pricing_with_bad_start_date():
    amount = 20
    starts = a_start_date.isoformat() # starts that conflicts
    assert_raises(Exception, pricinglib.pricings.new, (test_data.resource_id, test_data.plan_id, starts, amount))

def test_change_in_previous_pricing():
    # This checks if previous pricing date is adjusted or not
    previous_pricing_info = pricinglib.pricing.info(test_data.pricing_id)
    amount = 30
    start_date = a_end_date - datetime.timedelta(365)
    starts = start_date.isoformat()
    pricing_id  = pricinglib.pricings.new(test_data.resource_id, test_data.plan_id, starts, amount)
    previous_pricing_info_now = pricinglib.pricing.info(test_data.pricing_id)
    env.context.pgcursor.connection.commit()
    assert (start_date - previous_pricing_info_now.ends) == datetime.timedelta(1)

def test_add_pricing_for_a_plan_with_same_date():
    amount = 20
    test_data.price_w_plan = amount
    starts = a_start_date.isoformat()
    try:
        pricing_id  = pricinglib.pricings.new(test_data.resource_id, test_data.plan_id, starts, amount)
        # adding this pricing must work not next
    except Exception, err:
        assert True # isinstance(err, be.errors.ErrorWithHint)
    else:
        assert False

def test_add_pricing_for_default_tariff():
    amount = 50
    test_data.price_wo_plan = amount
    starts = a_start_date.isoformat()
    pricing_id = pricinglib.pricings.new(test_data.resource_id, test_data.default_tariff_id, starts, amount)
    info = pricinglib.pricing.info(pricing_id)
    test_data.default_pricing_id = pricing_id
    env.context.pgcursor.connection.commit()
    assert info.amount == amount

def test_add_member_w_plan_subscription():
    data = test_data.even_more_members[0]
    member_id = test_member.test_create_member(data)
    test_data.even_more_member_ids.append(member_id)
    starts = membership_starts.isoformat()
    ends = membership_ends.isoformat()
    created_by = test_data.admin
    assert membershiplib.memberships.new(test_data.plan_id, member_id, starts, ends) == True
    test_data.member_w_plan = member_id
    env.context.pgcursor.connection.commit()

def test_member_tariff():
    return pricinglib.member_tariff(test_data.member_w_plan, test_data.bizplace_id)

def test_add_member_wo_plan_subscription():
    data = test_data.even_more_members[1]
    member_id = test_member.test_create_member(data)
    test_data.even_more_member_ids.append(member_id)
    test_data.member_wo_plan = member_id
    env.context.pgcursor.connection.commit()

def test_get_pricing_for_member_w_plan():
    assert pricinglib.pricings.get(test_data.member_w_plan, test_data.resource_id, a_usage_time) == test_data.price_w_plan
    assert pricinglib.pricings.get(test_data.member_w_plan, test_data.resource_id, another_usage_time) == test_data.price_w_plan # Important to test membership end date as memberships only stores date and usage stores datetime so on membership end date usage.start_time is greater that membership.ends

def test_get_pricing_for_member_wo_plan():
    usage_time = datetime.datetime.now()
    assert pricinglib.get(test_data.member_wo_plan, test_data.resource_id, usage_time) == test_data.price_wo_plan

def test_cost():
    quantity = 10
    starts = datetime.datetime.now().isoformat()
    ends = (datetime.datetime.now() + datetime.timedelta(0, 10*3600)).isoformat()
    result = pricinglib.calculate_cost(test_data.member_w_plan, test_data.resource_id, test_data.bizplace_id, quantity, starts, ends, return_taxes=True)
    rate = pricinglib.pricings.get(test_data.member_w_plan, test_data.resource_id, starts)
    assert result['calculated_cost'] == costlib.to_decimal(float(quantity * rate))
    assert result['total'] == costlib.to_decimal(float(quantity * rate) * ( 100 + sum(test_data.taxes.values()) ) / 100 )

def test_calculate_taxes():
    result = pricinglib.apply_taxes(0, test_data.bizplace_id, 1000)
    assert result[0] == costlib.to_decimal("1125.00")
    for name, level, amount in result[1]['breakdown']:
        assert level == test_data.taxes[name]
    invoicepreflib.invoicepref_resource.update(test_data.bizplace_id, tax_included=True)
    result = pricinglib.apply_taxes(0, test_data.bizplace_id, 1000)
    assert result[0] == costlib.to_decimal("1000.00")
    total_tax_level = sum(map(float, test_data.taxes.values()))
    breakdown_dict = dict((name, amount) for name, level, amount in result[1]['breakdown'])
    for tax in test_data.taxes:
        assert round(breakdown_dict[tax]) == round(test_data.taxes[tax]*(1000/(100+total_tax_level)*100.0)/100.0)

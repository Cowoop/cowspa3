import commontest
from nose.tools import assert_raises
import test_data

import datetime
import be.apis.membership as membershiplib
import be.apis.usage as usagelib
import dateutil.relativedelta as relativedelta

today = datetime.date.today()

class months_data(): pass
months_data.first = (-10, -5)
months_data.non_ending = (-4, None)
months_data.ends_in_future = (1, 5)
months_data.non_ending2 = (6, None)
months_data.extend = 9
months_data.extend2 = 10

def test_create_membership():
    """
    must create usages till current month
    """
    member_id = test_data.membership_member_id
    tariff_id = test_data.plan_id
    starts_months, ends_months = months_data.first
    starts = today + relativedelta.relativedelta(months=starts_months)
    ends = today + relativedelta.relativedelta(months=ends_months)
    usages_before = usagelib.usage_collection.find(member_ids=[member_id])
    membershiplib.new(tariff_id, member_id, starts, ends)
    usages_after = usagelib.usage_collection.find(member_ids=[member_id])
    env.context.pgcursor.connection.commit()
    no_of_new_usages = len(usages_after) - len(usages_before)
    assert no_of_new_usages == (abs(starts_months) - abs(ends_months) + 1)

def test_create_membership_non_ending():
    """
    must create usages till current month
    """
    member_id = test_data.membership_member_id
    tariff_id = test_data.plan_id
    no_of_months, ends = months_data.non_ending
    starts = today + relativedelta.relativedelta(months=no_of_months)
    usages_before = usagelib.usage_collection.find(member_ids=[member_id])
    membershiplib.new(tariff_id, member_id, starts, ends)
    usages_after = usagelib.usage_collection.find(member_ids=[member_id])
    env.context.pgcursor.connection.commit()
    no_of_new_usages = len(usages_after) - len(usages_before)
    assert no_of_new_usages == (abs(no_of_months)+1)

def test_create_membership_w_future_end_date():
    """
    starts from current month with future ends date
    """
    member_id = test_data.membership_member_id
    tariff_id = test_data.plan_id
    starts_months, ends_months = months_data.ends_in_future
    starts = today + relativedelta.relativedelta(months=starts_months)
    ends = today + relativedelta.relativedelta(months=ends_months)
    usages_before = usagelib.usage_collection.find(member_ids=[member_id])
    membershiplib.new(tariff_id, member_id, starts, ends)
    usages_after = usagelib.usage_collection.find(member_ids=[member_id])
    env.context.pgcursor.connection.commit()
    no_of_new_usages = len(usages_after) - len(usages_before)
    assert no_of_new_usages == (ends_months - starts_months + 1)

def test_create_membership_w_no_end_date():
    """
    starts from current month. No usage should be created as usages are in future
    """
    member_id = test_data.membership_member_id
    tariff_id = test_data.plan_id
    starts_months, ends = months_data.non_ending2
    starts = today + relativedelta.relativedelta(months=starts_months)
    usages_before = usagelib.usage_collection.find(member_ids=[member_id])
    membershiplib.new(tariff_id, member_id, starts, ends)
    usages_after = usagelib.usage_collection.find(member_ids=[member_id])
    env.context.pgcursor.connection.commit()
    no_of_new_usages = len(usages_after) - len(usages_before)
    assert no_of_new_usages == 0

def create_membership_overlapping_start():
    """
    should fail
    """

def create_membership_overlapping_start_w_non_ending():
    """
    should shrink non_ending membership if possible
    """

def create_membership_overlapping_end():
    """
    """

def create_membership_overlapping_end_w_non_ending():
    """
    """

def delete_membership():
    """
    """

def shrink_membership():
    """
    """

def expand_membership():
    """
    """

def extend(bizplace_id, months=0):
    """
    months: months to add to today
    """
    member_id = test_data.membership_member_id
    date = today + relativedelta.relativedelta(months=months)
    usages_before = usagelib.usage_collection.find(member_ids=[member_id])
    membershiplib.autoextend(bizplace_id, date.month, date.year)
    usages_after = usagelib.usage_collection.find(member_ids=[member_id])
    return len(usages_after) - len(usages_before)

def test_autoextend():
    no_of_new_usages = extend(test_data.bizplace_id, months_data.extend)
    assert no_of_new_usages == 1

def test_autoextend_again():
    no_of_new_usages = extend(test_data.bizplace_id, months_data.extend)
    assert no_of_new_usages == 0

def test_autoextend_next():
    no_of_new_usages = extend(None, months_data.extend2)
    assert no_of_new_usages == 1

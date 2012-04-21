import commontest
from nose.tools import assert_raises
import test_data

import datetime
import be.repository.access as dbaccess
import be.apis.usage as usagelib
import be.apis.user as userlib
import be.apis.billingpref as billingpreflib
import be.apis.invoicepref as invoicepreflib
import be.errors
import be.libs.cost as costlib
import test_resources

usage_to_delete_late = None # booking can not be canceled if it is less than 14 days away
booking_id = None

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
    be.apis.user.set_context(test_data.member_id)

def test_add_usage():
    data = test_data.usage
    data['member'] = test_data.member_id
    data['resource_id'] = test_data.resource_id
    data['resource_owner'] = test_data.bizplace_id
    data['start_time'] = datetime.datetime.now().isoformat()
    data['end_time'] = datetime.datetime.now().isoformat()
    data['invoice'] = 1
    test_data.usage_id = usagelib.usage_collection.new(**data)
    usage = usagelib.usage_store.get(test_data.usage_id)
    env.context.pgcursor.connection.commit()
    assert isinstance(test_data.usage_id, (int, long))

def test_add_another_usage():
    global usage_to_delete_late
    data = test_data.usage
    data['member'] = test_data.more_member_ids[-1]
    data['resource_id'] = test_data.resource_id
    data['resource_owner'] = test_data.bizplace_id
    data['start_time'] = (datetime.datetime.now() + datetime.timedelta(1)).isoformat()
    data['end_time'] = (datetime.datetime.now() + datetime.timedelta(1)).isoformat()
    usage_to_delete_late = usagelib.usage_collection.new(**data)
    usage = usagelib.usage_store.get(usage_to_delete_late)
    env.context.pgcursor.connection.commit()
    assert isinstance(test_data.usage_id, (int, long))

def test_update_usage():
    old_cost = usagelib.usage_resource.get(test_data.usage_id, 'cost')
    new_cost = 2000
    mod_data = dict(cost=new_cost)
    usagelib.usage_resource.update(test_data.usage_id, **mod_data)
    env.context.pgcursor.connection.commit()
    assert old_cost == test_data.usage['cost']
    assert new_cost == usagelib.usage_resource.info(test_data.usage_id)['cost']

def test_delete_or_cancel_usage():
    usagelib.usage_resource.update(test_data.usage_id, invoice=50000) # TODO usage uninvoiced will be deleted not canceled so to test usage cancelation we are setting non existing invoice id
    old_amount = usagelib.usage_resource.get(test_data.usage_id, 'total')
    usage_id = usagelib.usage_collection.delete(test_data.usage_id)
    assert usagelib.usage_resource.get(test_data.usage_id, 'total') == old_amount
    assert usagelib.usage_resource.get(usage_id, 'cancelled_against') == test_data.usage_id
    assert usagelib.usage_resource.get(usage_id, 'total') == -old_amount
    assert usagelib.usage_collection.delete(usage_id) == True

def test_add_more_usage():
    resource_id = test_data.more_resource_ids[0]
    for data in test_data.more_usages:
        data['member'] = test_data.member_id
        data['resource_id'] = resource_id
        data['resource_owner'] = test_data.bizplace_id
        data['start_time'] = datetime.datetime.now().isoformat()
        data['end_time'] = datetime.datetime.now().isoformat()
        usage_id = usagelib.usage_collection.new(**data)
    env.context.pgcursor.connection.commit()

def test_add_booking():
    global booking_id
    now = datetime.datetime.now()
    data = dict(resource_id=test_data.resource_id) # time based resource
    data['resource_name'] = test_data.resource_data['name']
    data['member'] = test_data.member_id
    data['resource_owner'] = test_data.bizplace_id
    data['start_time'] = now.isoformat()
    data['end_time'] = (now + datetime.timedelta(0, 60*60)).isoformat()
    booking_id = usagelib.usage_collection.new(**data)
    env.context.pgcursor.connection.commit()

def test_extend_booking():
    info = usagelib.usage_resource.info(booking_id)
    old_total = info.total
    new_end_time = (info.end_time + datetime.timedelta(0, 60*60)).isoformat()
    usagelib.usage_resource.update(booking_id, end_time=new_end_time)
    new_total = usagelib.usage_resource.info(booking_id).total
    env.context.pgcursor.connection.commit()
    assert new_total == old_total * 2

def test_update_booking_custom_cost():
    info = usagelib.usage_resource.info(booking_id)
    old_total = info.total
    new_cost = old_total + 100
    usagelib.usage_resource.update(booking_id, cost=new_cost)
    usage = usagelib.usage_resource.info(booking_id)
    new_total = usage.total
    env.context.pgcursor.connection.commit()
    taxes = costlib.to_decimal(usage.tax_dict['total'])
    taxes_included = invoicepreflib.invoicepref_resource.info(test_data.bizplace_id).tax_included
    expected_total = new_cost if taxes_included else (new_cost + taxes)
    assert new_total != old_total
    assert new_total == expected_total

def test_find_by():
    data = dict(start=(datetime.datetime.now() - datetime.timedelta(1)), end=datetime.datetime.now())
    usages = usagelib.usage_collection.find(**data)
    assert len(usages) >= 4
    for usage in usages:
        assert usage['start_time'] >= data['start'] and usage['start_time'] <= data['end']

    data = dict(res_owner_ids=[test_data.bizplace_id])
    usages = usagelib.usage_collection.find(**data)
    assert bool(usages)

def test_uninvoiced():
    start = (datetime.datetime.now() - datetime.timedelta(1)).isoformat()
    end = datetime.datetime.now().isoformat()
    usages = usagelib.usage_collection.uninvoiced(member_id=test_data.member_id, start=start, end=end, res_owner_id=test_data.bizplace_id)
    usages_again = usagelib.usage_collection.uninvoiced(member_id=test_data.member_id, start=start, end=end, res_owner_id=test_data.bizplace_id)
    assert usages == usages_again # there is recursion used in finding billto member so just making sure
    #TODO we should make sure that all usage.member have billto pointing to member_id or usage.member == member_id
    assert len(usages) >= 1
    assert all((usage.member_id == test_data.member_id) for usage in usages)

def test_uninvoiced_billto():
    billing_member_id = test_data.more_member_ids[0]
    billto_member_id = test_data.member_id
    test_data.billing_member_id = billing_member_id
    test_data.billto_member_id = billto_member_id
    mode = billingpreflib.modes.other
    billingpreflib.billingpref_resource.update(member=billing_member_id, mode=mode, billto=billto_member_id)
    info = billingpreflib.billingpref_resource.info(billing_member_id)
    assert info.billto == billto_member_id
    start = (datetime.datetime.now() - datetime.timedelta(1)).isoformat()
    end = datetime.datetime.now().isoformat()
    usages = usagelib.usage_collection.uninvoiced(member_id=billto_member_id, start=start, end=end, res_owner_id=test_data.bizplace_id)
    assert all((usage.member_id in (billing_member_id, billto_member_id)) for usage in usages)

def test_uninvoiced_members():
    # 1. Add usage for member whose billto is set
    data = dict(resource_name='BILLTO Usage')
    data['member'] = test_data.billing_member_id
    data['resource_id'] = test_data.resource_id
    data['resource_owner'] = test_data.bizplace_id
    data['start_time'] = datetime.datetime.now().isoformat()
    data['end_time'] = datetime.datetime.now().isoformat()
    test_data.billto_usage['id'] = usagelib.usage_collection.new(**data)
    test_data.billto_usage['member'] = test_data.billing_member_id
    test_data.billto_usage['billto'] = test_data.billto_member_id
    assert isinstance(test_data.usage_id, (int, long))
    env.context.pgcursor.connection.commit()

    # 2. Find above usage in uninvoiced_members usage search
    start = (datetime.datetime.now() + datetime.timedelta(1)).isoformat()
    uninvoiced = usagelib.usage_collection.uninvoiced_members(res_owner_id=test_data.bizplace_id, start=start)
    uninvoiced_member_ids = []
    for member_uninvoiced in uninvoiced:
        this_member = member_uninvoiced['member']
        if this_member == test_data.billto_member_id:
            billto_usages = member_uninvoiced['usages']
        uninvoiced_member_ids.append(this_member)
        assert this_member != test_data.billing_member_id, 'billing member should not appear in uninvoiced'
        assert test_data.usage_id not in (usage.id for usage in member_uninvoiced['usages']) # test_data.usage_id is invoiced
    assert test_data.billto_member_id in uninvoiced_member_ids
    assert test_data.billto_usage['id'] in (usage.id for usage in billto_usages)

def test_delete_usage_unauthorized():
    current_user_id = env.context.user_id
    userlib.set_context(test_data.more_member_ids[-1])
    assert_raises(be.errors.SecurityViolation, usagelib.usage_collection.delete, 1)
    userlib.set_context(current_user_id)

def test_delete_usage_late():
    current_user_id = env.context.user_id
    userlib.set_context(test_data.more_member_ids[-1])
    assert_raises(be.errors.SecurityViolation, usagelib.usage_collection.delete, usage_to_delete_late)
    userlib.set_context(current_user_id)

def test_delete_usage():
    ret = usagelib.usage_collection.delete(1)
    assert ret == True

def test_custom_usage():
    data = test_data.usage
    data['member'] = test_data.member_id
    data['resource_id'] = 0
    data['resource_name'] = 'Test Custom Usage'
    data['resource_owner'] = test_data.bizplace_id
    data['start_time'] = datetime.datetime.now().isoformat()
    data['end_time'] = datetime.datetime.now().isoformat()
    test_data.usage_id = usagelib.usage_collection.new(**data)
    env.context.pgcursor.connection.commit()
    assert isinstance(test_data.usage_id, (int, long))

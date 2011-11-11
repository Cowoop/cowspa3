import datetime
import collections

import commonlib.helpers
import bases.app as applib
import be.repository.access as dbaccess
import be.apis.activities as activitylib

resource_store = dbaccess.stores.resource_store
bizplace_store = dbaccess.stores.bizplace_store
membership_store = dbaccess.stores.membership_store

membership = applib.Resource()
memberships = applib.Collection()

def new(tariff_id, subscriber_id, starts=None):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    old_sub = dbaccess.get_member_subscription(subscriber_id, bizplace.id, starts)
    starts =  commonlib.helpers.iso2date(starts) if starts else datetime.date.today()
    if old_sub:
        ends = starts - datetime.timedelta(1)
        if ends <= old_sub.starts.date():
            raise Exception("Start date must be greater than %s" % (old_sub.starts + datetime.timedelta(1)))
        membership_store.update_by(crit=dict(subscriber_id=subscriber_id, tariff_id=old_sub.tariff_id, starts=old_sub.starts), ends=ends)
    membership_store.add(tariff_id=tariff_id, starts=starts, subscriber_id=subscriber_id, bizplace_id=tariff.owner, \
        bizplace_name=bizplace.name, tariff_name=tariff.name)
    # find old subscription
    # set end date to it
    return True

def bulk_new(tariff_id, subscriber_ids, starts):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    for subscriber_id in subscriber_ids:
        new(tariff_id, subscriber_id, starts)
    return True

def list_by_tariff(tariff_id):
    """
    returns list of subscriber dicts.
    Subscriber Dict keys include following
    - member id
    - display name
    """
    member_list = []
    for m_dict in dbaccess.find_tariff_members([tariff_id]):
        m_dict['id'] = m_dict.pop('member')
        member_list.append(m_dict)
    return member_list

def list_for_member(member_id):
    memberships = dbaccess.get_member_subscriptions(member_id)
    for ms in memberships[::-1]:
        ms['starts'] = ms['starts'].isoformat()
        ms['ends'] =  ms['ends'].isoformat() if ms['ends'] else ms['ends']
    return memberships

def list(by_tariff=None, for_member=None):
    if by_tariff:
        return list_by_tariff(by_tariff)
    return list_for_member(for_member)

memberships.new = new
memberships.bulk_new = bulk_new
memberships.list = list_by_tariff

def info(subscription_id):
    """
    """
    return membership_store.get(subscription_id)

def delete(subscription_id):
    """
    """
    # Check if there are invoiced tariff usages
    return membership_store.destroy(subscription_id)

def stop(subscription_id, ends):
    """
    marks a subscription to stop given date and as necessary cancels/removes/chnages tariff usages associated with this subscription
    """
    # Remove extra uninvoiced usages
    return membership_store.update(subscription_id, ends=ends)

def update(subscription_id, **mod_data):
    """
    """
    return membership_store.update(subscription_id, **mod_data)

membership.info = info
membership.delete = delete
membership.stop = stop
membership.update = update

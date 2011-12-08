import datetime
import collections

import commonlib.helpers
import bases.app as applib
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.usage as usagelib

resource_store = dbaccess.stores.resource_store
bizplace_store = dbaccess.stores.bizplace_store
membership_store = dbaccess.stores.membership_store

membership = applib.Resource()
memberships = applib.Collection()

def new(tariff_id, member_id, created_by, starts=None):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    old_sub = dbaccess.get_member_membership(member_id, bizplace.id, starts)
    if starts:
        starts_dt = commonlib.helpers.iso2date(starts)
    else:
        starts_dt = datetime.date.today()
        starts =  starts_dt.isoformat()
    if old_sub:
        ends = starts_dt - datetime.timedelta(1)
        if ends <= old_sub.starts:
            raise Exception("Start date must be greater than %s" % (old_sub.starts + datetime.timedelta(1)))
        membership_store.update_by(crit=dict(member_id=member_id, tariff_id=old_sub.tariff_id, starts=old_sub.starts), ends=ends)
    membership_store.add(tariff_id=tariff_id, starts=starts_dt, member_id=member_id, bizplace_id=tariff.owner, \
        bizplace_name=bizplace.name, tariff_name=tariff.name)
    # find start, end dates for every months month in start-end and create that many usages
    # ex. starts: 3 Jan 2021 ends: 5 Apr 2021
    # usage 1: 3 Jan - 31 Jan 2021
    # usage 2: 1 Feb - 28 Feb 2021
    # usage 3: 1 Mar - 31 Mar 2021
    # usage 4: 1 Apr - 05 Apr 2021
    usagelib.usage_collection.new(tariff_id, tariff.name, member_id, starts, created_by)
    return True

def bulk_new(tariff_id, member_ids, created_by, starts):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    for member_id in member_ids:
        new(tariff_id, member_id, created_by, starts)
    return True

def list_by_tariff(tariff_id):
    """
    returns list of member dicts.
    Subscriber Dict keys include following
    - member id
    - display name
    """
    member_list = []
    for m_dict in dbaccess.find_tariff_members([tariff_id]):
        m_dict['id'] = m_dict.pop('member')
        member_list.append(m_dict)
    return member_list

def list_for_member(member_id, not_current=False):
    return dbaccess.get_member_memberships(member_id=member_id, not_current=not_current)

def list_memberships(by_tariff=None, for_member=None, not_current=False):
    if by_tariff:
        return list_by_tariff(by_tariff)
    return list_for_member(for_member, not_current)

memberships.new = new
memberships.bulk_new = bulk_new
memberships.list = list_memberships

def info(membership_id):
    """
    """
    return membership_store.get(membership_id)

def stop(membership_id, ends):
    """
    marks a membership to stop given date and as necessary cancels/removes/chnages tariff usages associated with this membership
    """
    # Remove extra uninvoiced usages
    return membership_store.update(membership_id, ends=ends)

def update(membership_id, **mod_data):
    """
    """
    return membership_store.update(membership_id, **mod_data)

def delete(membership_id):
    """
    """
    # Check if there are invoiced tariff usages
    return membership_store.remove(membership_id)

membership.info = info
membership.delete = delete
membership.stop = stop
membership.update = update

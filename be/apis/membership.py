import datetime
import collections
import calendar

import commonlib.helpers
import bases.app as applib
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.usage as usagelib
import be.apis.resource as resourcelib

resource_store = dbaccess.stores.resource_store
bizplace_store = dbaccess.stores.bizplace_store
membership_store = dbaccess.stores.membership_store

membership = applib.Resource()
memberships = applib.Collection()

def new(tariff_id, member_id, starts, ends):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    starts_dt = commonlib.helpers.iso2date(starts)
    ends_dt = commonlib.helpers.iso2date(ends)
    overlapping_membership = dbaccess.get_member_membership(member_id, bizplace.id, starts_dt)
    if starts_dt > ends_dt:
        raise Exception("End date should be greater than start date.")
    if overlapping_membership:
        raise Exception("Start date is overlapping with another membership.")
    overlapping_membership = dbaccess.get_member_membership(member_id, bizplace.id, ends_dt)
    if overlapping_membership:
        raise Exception("End date is overlapping with another membership.")
    membership_store.add(tariff_id=tariff_id, starts=starts_dt, ends=ends_dt,member_id=member_id,\
                         bizplace_id=tariff.owner, bizplace_name=bizplace.name, tariff_name=tariff.name)
    return create_membership_usages(starts_dt, ends_dt, tariff_id, tariff.name, member_id)

def create_membership_usages(starts, ends, tariff_id, tariff_name, member):
    # find start, end dates for every months month in start-end and create that many usages
    # ex. starts: 3 Jan 2021 ends: 5 Apr 2021
    # usage 1: 3 Jan - 31 Jan 2021
    # usage 2: 1 Feb - 28 Feb 2021
    # usage 3: 1 Mar - 31 Mar 2021
    # usage 4: 1 Apr - 05 Apr 2021
    while starts <= ends:
        if starts.month == ends.month:
            new_ends = ends
        else:
            new_ends = datetime.date(starts.year, starts.month, calendar.monthrange(starts.year, starts.month)[1])
        data = dict(resource_id=tariff_id, resource_name=tariff_name, member=member, start_time=starts.isoformat(), end_time=new_ends.isoformat())
        usagelib.usage_collection.new(**data)
        starts = new_ends + datetime.timedelta(1)
    return True
    
def bulk_new(tariff_id, member_ids, starts, ends):
    """
    """
    tariff = resource_store.get(tariff_id)
    bizplace = bizplace_store.get(tariff.owner)
    for member_id in member_ids:
        new(tariff_id, member_id, starts, ends)
    return True

def list_by_tariff(tariff_id, at_time=None):
    """
    returns list of member dicts.
    Subscriber Dict keys include following
    - member id
    - display name
    """
    at_time = commonlib.helpers.iso2date(at_time) if at_time else at_time
    member_list = []
    for m_dict in dbaccess.find_tariff_members([tariff_id], at_time):
        m_dict['id'] = m_dict.pop('member')
        member_list.append(m_dict)
    return member_list

def list_for_member(member_id, not_current=False):
    return dbaccess.get_member_memberships(member_id=member_id, not_current=not_current)

def list_memberships(by_tariff=None, for_member=None, not_current=False, at_time=None):
    if by_tariff:
        return list_by_tariff(by_tariff, at_time)
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
    return update(membership_id, ends=ends, stopped=True)
    
def update(membership_id, **mod_data):
    """
    """
    old_data = info(membership_id)
    usages = usagelib.usage_collection.find(start=old_data['starts'], end=old_data['ends'], member_ids=[old_data['member_id']], resource_ids=[old_data['tariff_id']], only_non_cancelled=True)
    starts = commonlib.helpers.iso2date(mod_data['starts']) if 'starts' in mod_data else old_data['starts']
    ends = commonlib.helpers.iso2date(mod_data['ends']) if 'ends' in mod_data else old_data['ends']
    
    #Checking that new starts & ends are valid or not
    if starts > ends:
        raise Exception("End date should be greater than start date.")
    overlapping_membership = dbaccess.get_member_membership(old_data['member_id'], old_data['bizplace_id'], starts,\
     [membership_id])
    if overlapping_membership:
        raise Exception("Start date is overlapping with another membership.")
    overlapping_membership = dbaccess.get_member_membership(old_data['member_id'], old_data['bizplace_id'], ends,\
     [membership_id])
    if overlapping_membership:
        raise Exception("End date is overlapping with another membership.")
        
    #Deleting usages which are out of starts<->ends
    rev_usages = range(len(usages)-1, -1, -1)
    for i in rev_usages:
        if usages[i]['start_time'].date() < starts or usages[i]['end_time'].date() > ends:
            usagelib.usage_collection.delete(usages[i]['id'])
            del(usages[i])
            
    #Creating new membership usages
    if usages:
        if starts != usages[0]['start_time'].date():
            create_membership_usages(starts, (usages[0]['start_time']-datetime.timedelta(1)).date(),\
             old_data['tariff_id'], old_data['tariff_name'], old_data['member_id'])
        if ends != usages[-1]['end_time'].date():
            create_membership_usages((usages[-1]['end_time']+datetime.timedelta(1)).date(), ends,\
             old_data['tariff_id'], old_data['tariff_name'], old_data['member_id'])
    else:
        create_membership_usages(starts, ends, old_data['tariff_id'], old_data['tariff_name'], old_data['member_id'])
    
    return membership_store.update(membership_id, **mod_data)

def delete(membership_id):
    """
    """
    membership = info(membership_id)
    usages = usagelib.usage_collection.find(start=membership['starts'], end=membership['ends'], member_ids=[membership['member_id']], resource_ids=[membership['tariff_id']], only_non_cancelled=True)
    usagelib.usage_collection.bulk_delete([usage.id for usage in usages])
    return membership_store.remove(membership_id)
    
membership.info = info
membership.delete = delete
membership.stop = stop
membership.update = update

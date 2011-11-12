import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import commonlib.helpers

bizplace_store = dbaccess.bizplace_store
plan_store = dbaccess.resource_store
membership_store = dbaccess.membership_store

class PlanCollection:

    def new(self, name, bizplace_id, short_description='', long_description=''):
        created = datetime.datetime.now()
        data = dict(name=name, bizplace=bizplace_id, short_description=short_description, long_description=long_description, created=created)
        tariff_id = plan_store.add(**data)

        data = dict(name=name, id=tariff_id, bizplace=bizplace_store.get(bizplace_id, ['name']))
        activity_id = activitylib.add('plan_management', 'plan_created', data, created)
        return tariff_id

    def delete(self, tariff_id):
        """
        Deletes a plan. Only if there are no members.
        """

    def list(self, bizplace_id):
        """
        returns list of plans which are at bizplace_id
        """
        return plan_store.get_by(crit=dict(bizplace=bizplace_id), fields=['id', 'name', 'short_description'])

class PlanResource:

    def info(self, tariff_id):
        """
        """
        return plan_store.get(tariff_id, dbaccess.plan_info_fields)


    def details(self, tariff_id):
        """
        """
        d = info(tariff_id)
        d['members'] = self.members(tariff_id)
        return d

    def update(self, tariff_id, mod_data):
        """
        """

    def members(self, tariff_id):
        """
        returns list of member dicts.
        Subscriber Dict keys include following
        - member id
        - display name
        """
        member_list = []
        for m_dict in dbaccess.find_plan_members([tariff_id]):
            m_dict['id'] = m_dict.pop('member')
            member_list.append(m_dict)
        return member_list

    def new_member(self, tariff_id, member_id, starts=None):
        """
        """
        plan = plan_store.get(tariff_id)
        bizplace = bizplace_store.get(plan.bizplace)
        old_sub = dbaccess.get_member_membership(member_id, bizplace.id, starts)
        starts =  commonlib.helpers.iso2date(starts) if starts else datetime.date.today()
        if old_sub:
            ends = starts - datetime.timedelta(1)
            if ends <= old_sub.starts.date():
                raise Exception("Start date must be greater than %s" % (old_sub.starts + datetime.timedelta(1)))
            membership_store.update_by(crit=dict(member_id=member_id, tariff_id=old_sub.tariff_id, starts=old_sub.starts), ends=ends)
        membership_store.add(tariff_id=tariff_id, starts=starts, member_id=member_id, bizplace_id=plan.bizplace, \
            bizplace_name=bizplace.name, plan_name=plan.name)
        # find old membership
        # set end date to it
        return True

    def new_members(self, tariff_id, member_ids, starts):
        """
        """
        plan = plan_store.get(tariff_id)
        bizplace = bizplace_store.get(plan.bizplace)
        for member_id in member_ids:
            self.new_member(tariff_id, member_id, starts)
        return True

    def get_member_memberships(self, member_id):
        memberships = dbaccess.get_member_memberships(member_id)
        for ms in memberships[::-1]:
            ms['starts'] = ms['starts'].isoformat()
            ms['ends'] =  ms['ends'].isoformat() if ms['ends'] else ms['ends']
        return memberships

    def remove_member(self, membership_id):
        """
        """
        return membership_store.remove(membership_id)

    def change_membership(self, membership_id, **mod_data):
        """
        """
        return membership_store.update(membership_id, **mod_data)

plan_collection = PlanCollection()
plan_resource = PlanResource()

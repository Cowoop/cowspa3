import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib

biz_store = dbaccess.biz_store
bizplace_store = dbaccess.bizplace_store
plan_store = dbaccess.plan_store
subscription_store = dbaccess.subscription_store

class PlanCollection:

    def new(self, name, bizplace_id, description=''):
        created = datetime.datetime.now()
        data = dict(name=name, bizplace=bizplace_id, description=description, created=created)
        plan_id = plan_store.add(**data)
        
        data = dict(name=name, id=plan_id, bizplace=bizplace_store.get(bizplace_id, ['name']))
        activity_id = activitylib.add('plan_management', 'plan_created', data, created)
        return plan_id

    def delete(self, plan_id):
        """
        Deletes a plan. Only if there are no subscribers.
        """

    def list(self, bizplace_id):
        """
        returns list of plans which are at bizplace_id
        """
        return plan_store.get_by(crit=dict(bizplace=bizplace_id), fields=['id', 'name', 'description'])

class PlanResource:

    def info(self, plan_id):
        """
        """
        return plan_store.get(plan_id, dbaccess.plan_info_fields)


    def details(self, plan_id):
        """
        """
        d = info(plan_id)
        d['subscribers'] = subscribers(plan_id)
        return d

    def update(self, plan_id, mod_data):
        """
        """

    def subscribers(self, plan_id):
        """
        returns list of subscriber dicts.
        Subscriber Dict keys include following
        - member id
        - display name
        """
        member_list = []
        for m_dict in dbaccess.find_plan_members([plan_id]):
            m_dict['id'] = m_dict.pop('member')
            member_list.append(m_dict)
        return member_list

    def new_subscriber(self, plan_id, starts, subscriber_id):
        """
        """
        plan = plan_store.get(plan_id)
        bizplace = bizplace_store.get(plan.bizplace)
        old_sub = dbaccess.get_member_subscription(subscriber_id, bizplace.id, starts)
        if old_sub:
            if isinstance(starts, basestring):
                starts = datetime.datetime.strptime(starts, "%Y-%m-%dT%H:%M:%S")
            ends = starts - datetime.timedelta(1)
            if ends <= old_sub.starts.date():
                raise Exception("Start date must be greater than %s" % (old_sub.starts + datetime.timedelta(1)))
            subscription_store.update_by(crit=dict(subscriber_id=subscriber_id, plan_id=old_sub.plan_id, starts=old_sub.starts), ends=ends)
        subscription_store.add(plan_id=plan_id, starts=starts, subscriber_id=subscriber_id, bizplace_id=plan.bizplace, \
            bizplace_name=bizplace.name, plan_name=plan.name)
        # find old subscription
        # set end date to it
        return True

    def new_subscribers(self, plan_id, starts, subscriber_ids):
        """
        """
        plan = plan_store.get(plan_id)
        bizplace = bizplace_store.get(plan.bizplace)
        for subscriber_id in subscriber_ids:
            self.new_subscriber(plan_id, starts, subscriber_id)
        return True


    def remove_subscriber(self, subscription_id):
        """
        """
        return subscription_store.remove(subscription_id)

    def change_subscription(self, subscription_id, **mod_data):
        """
        """
        if 'starts' in mod_data:
            mod_data['starts'] = datetime.datetime.strptime(mod_data['starts'], "%Y-%m-%dT%H:%M:%S")
        if 'ends' in mod_data and mod_data['ends'] != "":
            mod_data['ends'] = datetime.datetime.strptime(mod_data['ends'], "%Y-%m-%dT%H:%M:%S")
        return subscription_store.update(subscription_id, **mod_data)
        
plan_collection = PlanCollection()
plan_resource = PlanResource()

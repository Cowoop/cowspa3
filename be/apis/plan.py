import datetime
import be.repository.access as dbaccess

biz_store = dbaccess.biz_store
bizplace_store = dbaccess.bizplace_store
plan_store = dbaccess.plan_store
subscription_store = dbaccess.subscription_store

class PlanCollection:

	def new(self, name, bizplace_id, description=''):
		created = datetime.datetime.now()
    		data = dict(name=name, bizplace=bizplace_id, description=description, created=created)
    		plan_id = plan_store.add(**data)
    		return plan_id

	def delete(self, plan_id):
    		"""
    		Deletes a plan. Only if there are no subscribers.
    		"""

class PlanResource:

	def info(self, plan_id):
    		"""
    		"""
    		return plan_store.get(plan_id)


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

	def new_subscriber(self, plan_id, subscriber_id):
    		"""
    		"""
    		plan = plan_store.get(plan_id)
    		bizplace = bizplace_store.get(plan.bizplace)
    		subscription_store.add(plan_id=plan_id, subscriber_id=subscriber_id, bizplace_id=plan.bizplace, \
        		bizplace_name=bizplace.name, plan_name=plan.name)
    		return True

	def new_subscribers(self, plan_id, subscriber_ids):
    		"""
    		"""
    		plan = plan_store.get(plan_id)
    		bizplace = bizplace_store.get(plan.bizplace)
    		for subscriber_id in subscriber_ids:
        		subscription_store.add(plan_id=plan_id, subscriber_id=subscriber_id, bizplace_id=plan.bizplace, \
            		bizplace_name=bizplace.name, plan_name=plan.name)
    		return True


	def remove_subscriber(self, plan_id, subscriber_id):
    		"""
    		"""

	def change_subscription(self, subscriber_id, current_plan_id, new_plan_id, change_date):
    		"""
    		"""
plan_collection = PlanCollection()
plan_resource = PlanResource()

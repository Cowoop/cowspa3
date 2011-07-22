import commonlib.shared.states
import be.repository.access as dbaccess
import bases.app
import pickle

activity_store = dbaccess.stores.activity_store

class ActivityCollection:

    category = dict( 
        MemberManagement = dict( 
            MemberCreated = 'New member created %(name)s.',
            MemberUpdated = '%(attrs)s updated by %(user_id)s.', 
            MemberDeleted = '%(name)s member deleted.'
            ),
        Security = dict( 
            PasswordChanged = 'Password changed by %(name)s.'
            )
        )
    
    def add(self, category, name, actor, data, created):

        data = dict(category=category, name=name, actor=actor, data=pickle.dumps(data), created=created)
        activity_id = activity_store.add(**data)
        return activity_id
    
    def find_activities_by_categories(self, categories, from_date, to_date):
        
        activity = dbaccess.Activity()
        activities = activity.list_by_categories(categories, from_date, to_date)
        msg_list = []
        for act in activities:
            msg_list.append(self.category[act['category']][act['name']] % pickle.loads(act['data']))
        return msg_list 
        
    def find_activities_by_name(self, name, from_date, to_date):
    
        activity = dbaccess.Activity()
        activities = activity.list_by_name(name, from_date, to_date)
        msg_list = []
        for act in activities:
            msg_list.append(self.category[act['category']][act['name']] % pickle.loads(act['data']))
        return msg_list

activity_collection = ActivityCollection()

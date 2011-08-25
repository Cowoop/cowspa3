import itertools
import datetime
import be.repository.access as dbaccess

activity_store = dbaccess.stores.activity_store

class Categories(dict):
    """
    subclassing dict to guarantee uniqueness of event name
    """
    def __init__(self, *args, **kw):
        super(Categories, self).__init__(*args, **kw)
        self.all_eventnames = tuple(itertools.chain(*(v.keys() for v in self.values())))
        for eventname in self.all_eventnames:
            if self.all_eventnames.count(eventname) > 1:
                raise Exception("Event name not unique: " + eventname)

categories = Categories(
    MemberManagement = dict(
        MemberCreated = 'New member created %(name)s.',
        MemberUpdated = '%(attrs)s updated by %(user_id)s.',
        MemberDeleted = '%(name)s member deleted.'
        ),
    Security = dict(
        PasswordChanged = 'Password changed by %(name)s.'
        )
    )

role_activities = dict(
    admin = dict( MemberManagement = ['MemberUpdated'], Security = []),
    member = dict( MemberManagement = ['MemberUpdated', 'MemberCreated'], Security = ['PasswordChanged'])
    )

def add(category, name, actor, data, created):

    data = dict(category=category, name=name, actor=actor, data=data, created=created)
    activity_id = activity_store.add(**data)
    return activity_id

def delete(activities):
    return activity_store.remove_many(activities)

def find_activities_by_categories(category_list, from_date, to_date, limit=30):

    activities = dbaccess.list_activities_by_categories(category_list, from_date, to_date)
    msg_list = []
    for act in activities:
        msg_list.append(categories[act['category']][act['name']] % act['data'])
    return msg_list

def find_activities_by_names(names, from_date, to_date, limit=30):

    activities = dbaccess.list_activities_by_names(names, from_date, to_date, limit)
    msg_list = []
    for act in activities:
        msg_list.append(categories[act['category']][act['name']] % act['data'])
    return msg_list
 
def find_role_activities(from_date, to_date, limit=10):
    
    names = []
    roles = env.context.roles
    for role in roles:
        for category in categories:
            if role_activities[role][category]:
                 for activity in role_activities[role][category]:
                    names.append(activity)
            else:
                 for activity in categories[category]:
                    names.append(activity)
    return find_activities_by_names(list(set(names)), from_date, to_date, limit)
    
def get_current_activities():
    
    from_date = datetime.datetime(2011,01,01,00,00,00) 
    to_date = datetime.datetime.now()
    return find_role_activities(from_date, to_date, 10)
    

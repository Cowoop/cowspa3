import datetime
import be.repository.access as dbaccess

import events

activity_store = dbaccess.stores.activity_store
activityaccess_store = dbaccess.stores.activityaccess_store
member_store = dbaccess.stores.member_store

def add(category, name, data, created=None):
    if not hasattr(env.context, 'user_id'): # while invoking apis directly. possibly in interactive session or test suites
        # warn
        return
    if not created:
        created = datetime.datetime.now()
    actor_id = env.context.user_id
    data['actor_name'] = env.context.name
    activity_id = activity_store.add(category=category, name=name, actor=actor_id, data=data, created=created)
    Event = events.categories[category][name]
    event = Event(env.context.user_id, created, data)
    access_items = []
    if 'roles' in event.access:
        for role_id, role_name in event.access['roles']:
            access_items.append(dict(a_id=activity_id, role_ctx=role_id, role_name=role_name, member_id=None))
    if 'member_ids' in event.access:
        access_items += [dict(a_id=activity_id, role_name=None, role_ctx=None, member_id=member_id) for member_id in event.access['member_ids']]
    activityaccess_store.add_many(access_items)
    return activity_id

def delete(activity_ids):
    activity_store.remove_many(activity_ids)
    for a_id in activity_ids:
        activityaccess_store.remove_by(crit=dict(a_id=a_id))

def get_latest(for_member=None, limit=30):
    # must secure it using wrappers
    for_member = for_member if for_member else env.context.user_id
    if for_member == env.context.user_id:
        roles = env.context.roles
    else:
        roles = [row[0] for row in userrole_store.get_by(crit=dict(user_id=for_member), fields=['role'], hashrows=False)]
    activities = dbaccess.find_activities([for_member], roles)
    messages = []
    for act in activities:
        event = events.categories[act.category][act.name](act.actor, act.created, act.data)
        messages.append(dict(message=event.message, tags=event.tags))
    return messages

def find_activities_by_categories(category_list, from_date, to_date, limit=30):

    activities = dbaccess.list_activities_by_categories(category_list, from_date, to_date)
    msg_list = []
    for act in activities:
        event = categories[act['category']][act['name']](act['data'])
        msg_list.append(event.message)
    return msg_list

def find_activities_by_names(names, from_date, to_date, limit=30):

    activities = dbaccess.list_activities_by_names(names, from_date, to_date, limit)
    msg_list = []
    for act in activities:
        event = categories[act['category']][act['name']](act['data'])
        msg_list.append(event.message)
    return msg_list

def find_role_activities(from_date, to_date, limit=10):
    names = []
    roles = env.context.roles
    for role in roles:
        for category in categories:
            if role_categories[role][category]:
                 for activity in role_categories[role][category]:
                    names.append(activity)
            elif role in role_categories:
                 for activity in categories[category]:
                    names.append(activity)
    return find_activities_by_names(list(set(names)), from_date, to_date, limit)

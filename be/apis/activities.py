import be.repository.access as dbaccess

activity_store = dbaccess.stores.activity_store

categories = dict(
    MemberManagement = dict(
        MemberCreated = 'New member created %(name)s.',
        MemberUpdated = '%(attrs)s updated by %(user_id)s.',
        MemberDeleted = '%(name)s member deleted.'
        ),
    Security = dict(
        PasswordChanged = 'Password changed by %(name)s.'
        )
    )

def add(category, name, actor, data, created):

    data = dict(category=category, name=name, actor=actor, data=dbaccess.PGBinary.to_pg(data), created=created)
    activity_id = activity_store.add(**data)
    return activity_id

def find_activities_by_categories(category_list, from_date, to_date):

    activities = dbaccess.list_activities_by_categories(category_list, from_date, to_date)
    msg_list = []
    for act in activities:
        msg_list.append(categories[act['category']][act['name']] % cPickle.loads(str(act['data'])))
    return msg_list

def find_activities_by_name(name, from_date, to_date):

    activities = dbaccess.list_activities_by_name(name, from_date, to_date)
    msg_list = []
    for act in activities:
        msg_list.append(categories[act['category']][act['name']] % dbaccess.PGBinary.to_python(act['data']))
    return msg_list


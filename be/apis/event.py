import be.repository.access as dbaccess

event_store = dbaccess.stores.event_store

def new(start_time, end_time, name=None, description=None, no_of_people=0, public=False):
    return event_store.add(name=name, description=description, start_time=start_time, end_time=end_time, no_of_people=no_of_people, public=public)

def update(event_id, **mod_data):
    event_store.update(event_id, **mod_data)

def delete(event_id):
    return event_store.remove(event_id)

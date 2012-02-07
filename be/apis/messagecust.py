import be.repository.access as db access

cust_message_store = access.stores.cust_message_store

def new(owner_id, name, content):
    return cust_message_store.new(owner=owner_id, name=name, content=content)

def get(name, owner_id):
    return cust_message_store.get_one_by(crit=dict(owner=owner_id, name=name))

def list(owner_id):
    return cust_message_store.get_by(crit=dict(owner=owner_id, name=name))

def update(name, owner_id, content):
    #msg = get(name, owner_id)
    # TODO send notification with old content
    cust_message_store.update_by(crit=dict(owner=owner_id, name=name), content=content)

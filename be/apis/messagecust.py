import be.repository.access as dbaccess

messagecust_store = dbaccess.stores.messagecust_store

def new(owner_id, name, content):
    return messagecust_store.new(owner=owner_id, name=name, content=content)

def get(name, owner_id):
    return messagecust_store.get_one_by(crit=dict(owner=owner_id, name=name))

def list(owner_id):
    return messagecust_store.get_by(crit=dict(owner=owner_id, name=name))

def update(name, owner_id, content):
    #msg = get(name, owner_id)
    # TODO send notification with old content
    messagecust_store.update_by(crit=dict(owner=owner_id, name=name), content=content)

import os.path
import be.repository.access as dbaccess
import commonlib.messaging.messages

messagecust_store = dbaccess.stores.messagecust_store

def new(owner_id, name, content):
    return messagecust_store.add(owner=owner_id, name=name, content=content)

def get(owner_id, name):
    mcust = messagecust_store.get_one_by_safe(crit=dict(owner=owner_id, name=name))
    return mcust.content if mcust else getattr(commonlib.messaging.messages, name).content_dict['plain']

def list(owner_id): # TODO: support names
    return messagecust_store.get_by(crit=dict(owner=owner_id, name=name))

def update(owner_id, name, content):
    #msg = get(name, owner_id)
    # TODO send notification with old content
    if get(owner_id, name):
        messagecust_store.update_by(crit=dict(owner=owner_id, name=name), content=content)
    else:
        new(owner_id, name, content)

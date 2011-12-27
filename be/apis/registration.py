import datetime
import be.repository.access as dbaccess
import commonlib.helpers
import be.apis.activities as activitylib
import be.apis.user as userlib
import be.apis.member as memberlib
import commonlib.messaging.messages as messages
import be.apis.activities as activitylib

user_store = dbaccess.stores.user_store
member_store = dbaccess.stores.member_store
registered_store = dbaccess.stores.registered_store

def _new(first_name, last_name, email):
    activation_key = commonlib.helpers.random_key_gen()
    created = datetime.datetime.now()
    registered_id = registered_store.add(activation_key=activation_key, first_name=first_name, last_name=last_name, email=email)
    activation_url = env.config.http_baseurl + "/activate#" + activation_key
    return activation_url

def new(first_name, last_name, email, sendmail=True):
    activation_url = _new(first_name, last_name, email)
    data = dict (first_name=first_name, activation_url=activation_url)
    mail_data = messages.activation.build(data)
    mail_data['to'] = (first_name, email)
    env.mailer.send(**mail_data)
    activitylib.add('member_management', 'new_registration', data)
    return registered_id

def activate(key, username, password):
    reg_info = info(key)
    userlib.set_context(env.config.system_username)
    member_id = memberlib.member_collection.new(reg_info.email, username, password, reg_info.first_name, last_name=reg_info.last_name)
    registered_store.remove_by(dict(activation_key=key))
    return member_id

def invite(first_name, last_name, email):
    activation_url = _new(first_name, last_name, email)
    data = dict(first_name=first_name, last_name=last_name, email=email, inviter_name=env.context.name, inviter_id=env.context.user_id, \
        activation_url=activation_url)
    mail_data = messages.invitation.build(data)
    mail_data['to'] = (first_name, email)
    env.mailer.send(**mail_data)
    activitylib.add('member_management', 'member_invited', data)

def info(key_or_id):
    if isinstance(key_or_id, basestring):
        return registered_store.get_one_by(dict(activation_key=key_or_id))
    return registered_store.get_one_by(dict(id=key_or_id))

def list():
    return registered_store.get_all()

def delete(key):
    registered_store.remove_by(activation_key=key)

def get(key, attrname):
    return registered_store.get_one_by(activation_key=key, fields=[attrname])

def update(key, **mod_data):
    registered_store.update_by(activation_key=key, fields=[attrname])

def set(key, attrname, v):
    update(key, attrname=v)

def search(q, options={}, limit=None):
    raise NotImplemented

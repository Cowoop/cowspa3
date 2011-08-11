import datetime
import commonlib
import be.repository.access as dbaccess
import be.errors as errors
import commonlib.helpers as helpers
import be.apis.member as memberlib
import be.apis.role as rolelib

user_store = dbaccess.stores.user_store
session_store = dbaccess.stores.session_store

def authenticate(username, password):
    """
    Returns T if authentication is successful. Else False.
    """
    try:
        passphrase = dbaccess.get_passphrase_by_username(username)
    except IndexError, err:
        return False
    encrypted = helpers.encrypt(password)
    return encrypted == passphrase

def create_session(user_id):
    token  = commonlib.helpers.random_key_gen()
    created = datetime.datetime.now()
    session_store.add(token=token, user_id=user_id, created=created)
    return token

def get_or_create_session(username):
    user = user_store.get_one_by(crit=dict(username=username))
    try:
        session = session_store.get_one_by(crit=dict(user_id=user.id))
        token = session.token
    except IndexError:
        token = create_session(user.id)
    return token

def session_lookup(token):
    try:
        session = session_store.get_one_by(crit=dict(token=token))
        user_id = session.user_id
    except IndexError:
        user_id = None
    return user_id

def login(username, password):
    if authenticate(username, password):
        return get_or_create_session(username)
    raise errors.ErrorWithHint('Authentication failed')

def set_context(session_id):
    env.context.user_id = session_lookup(session_id)

def logout(token):
    try:
        session = session_store.get_one_by(token=token)
        session.delete()
    except Exception, err:
        print err

def create_superuser(username, password, email, first_name, context):
    member_data = dict(username=username, password=password, email=email, first_name=first_name)
    user_id = memberlib.member_collection.new(**member_data)
    role_data = dict(user_id=user_id, roles=['admin'], context=context)
    return rolelib.assign(**role_data)
    

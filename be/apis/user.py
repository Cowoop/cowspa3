import datetime
import commonlib.shared.constants
import be.repository.access as dbaccess
import be.errors as errors
import commonlib.helpers as helpers
import be.apis.role as rolelib

user_store = dbaccess.stores.user_store
session_store = dbaccess.stores.session_store

def encrypt(phrase):
    return commonlib.helpers.encrypt(phrase, env.config.random_str)

def authenticate(username, password):
    """
    Returns T if authentication is successful. Else False.
    """
    try:
        passphrase = dbaccess.get_passphrase_by_username(username)
    except IndexError, err:
        return False
    encrypted = encrypt(password)
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
        auth_token = get_or_create_session(username)
        set_context(username)
        return auth_token
    raise errors.ErrorWithHint('Authentication failed')

def set_context(id_or_username):
    if isinstance(id_or_username, basestring):
        user = user_store.get_one_by(dict(username=id_or_username))
    else:
        user = user_store.get(id_or_username)
    env.context.user_id = user.id
    roles = dbaccess.userrole_store.get_by(dict(user_id = env.context.user_id), ['role'], False)
    env.context.roles = [role[0] for role in roles]
    try:
        env.context.display_name = member_store.get(env.context.user_id, fields=['display_name'])
    except:
        env.context.display_name = user.username

def set_context_by_session(session_id):
    set_context(session_lookup(session_id))

def logout(token):
    try:
        session = session_store.get_one_by(token=token)
        session.delete()
    except Exception, err:
        print err

def new(username, password, state=None):
    if state is None:
        state = commonlib.shared.constants.member.enabled
    user_id = dbaccess.OidGenerator.next("Member")
    data = dict(id=user_id, username=username, password=encrypt(password), state=state)
    user_store.add(**data)
    return user_id

def create_system_account():
    username = env.config.system_username
    password = commonlib.helpers.random_key_gen()
    user_id = new(username, password)
    rolelib.assign(user_id, ['admin'])
    return user_id

def get_user_preferences():
    return dbaccess.stores.memberpref_store.get_by(dict(member=env.context.user_id), ['theme', 'language'])[0]

import datetime
import hashlib
import commonlib.shared.constants
import be.repository.access as dbaccess
import be.errors as errors
import commonlib.helpers as helpers
import be.apis.role as rolelib
from be.libs.accesscontrol import Anonymous

user_store = dbaccess.stores.user_store
session_store = dbaccess.stores.session_store
member_store = dbaccess.stores.member_store

def new(username, password, enabled=True, enc_password=None):
    if enc_password:
        encrypted = enc_password
    else:
        if password is None:
            password = helpers.random_key_gen()
        encrypted = encrypt(password)
    user_id = dbaccess.OidGenerator.next("Member")
    data = dict(id=user_id, username=username, password=encrypted, enabled=enabled)
    user_store.add(**data)
    return user_id

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
    return passphrase == encrypted or passphrase == hashlib.md5(password).hexdigest()

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

def login(username=None, password=None, auth_token=None):
    if username:
        if authenticate(username, password):
            auth_token = get_or_create_session(username)
            set_context(username, None)
            return dict(auth_token=auth_token, \
                id=env.context.user_id, roles=env.context.roles, name=env.context.name, pref=get_user_preferences(env.context.user_id))
    elif auth_token:
        set_context_by_session(auth_token)
        return dict(auth_token=auth_token, \
                id=env.context.user_id, roles=env.context.roles, name=env.context.name, pref=get_user_preferences(env.context.user_id))
    raise errors.ErrorWithHint('Authentication failed')

login.access = Anonymous()

def set_context(id_or_username, context_id=0):
    """
    user_id: user.id
    name: name of the current user
    id: context_id
    current_roles: {context1: { ctx: context_id,
                                ctx_label: <context-label>,
                                ctx_roles: (
                                        {name: <role-name>, order: <role-order>, label: <role-label>},
                                        {name: <role-name>, order: <role-order>, label: <role-label>}, .. ),
                                role_names: (<role-name1>, <role-name2>, <role-name3>, ..) }
                    context2: {..},
                    ..
                    }
    """
    if isinstance(id_or_username, basestring):
        user = user_store.get_one_by(dict(username=id_or_username))
    else:
        user = user_store.get(id_or_username)
    env.context.user_id = user.id
    env.context.roles = rolelib.get_roles(user.id)
    current_roles = {}
    for role in env.context.roles:
        context = role['context']
        current_roles[context] = commonlib.helpers.odict(ctx=context, ctx_label=role['label'])
        current_roles[context]['ctx_roles'] = \
            tuple(dict(name=ctx_role['role'], order=ctx_role['order'], label=ctx_role['label']) for ctx_role in role['roles'])
        current_roles[context]['role_names'] = set(ctx_role['role'] for ctx_role in role['roles'])
    env.context.current_roles = current_roles
    env.context.current_perms = rolelib.permissions_by_current_roles()
    try:
        env.context.name = member_store.get(env.context.user_id, fields=['name'])
    except:
        env.context.name = user.username
    env.context.id = context_id

def set_context_by_session(session_id, context_id=0):
    set_context(session_lookup(session_id), context_id)

def logout(token):
    try:
        session = session_store.get_one_by(token=token)
        session.delete()
    except Exception, err:
        print err

def update(member_id, **mod_data):
    if 'password' in mod_data: mod_data['password'] = encrypt(mod_data['password'])
    user_store.update(member_id, **mod_data)

def create_system_account():
    username = env.config.system_username
    password = commonlib.helpers.random_key_gen()
    user_id = new(username, password)
    rolelib.new_roles(user_id, ['admin'], 0)
    return user_id

def get_user_preferences(user_id):
    return dbaccess.stores.memberpref_store.get_by(dict(member=user_id), ['theme', 'language'])[0]

def is_host():
    #set_context_by_session(session_id)
    for role in env.context.roles:
        ctx_roles = role['roles']
        for ctx_role in ctx_roles:
            if ctx_role['role'] in ('admin', 'host', 'director'):
                return True

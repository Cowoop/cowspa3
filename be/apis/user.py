import be.repository.access as dbaccess
import commonlib.helpers as helpers

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
    session_store.add(token, user_id)
    return token

def get_or_create_session(username):
    user = userstore.get_one_by(username=username)
    try:
        session = session_store.get_one_by(user_id=user.id)
        token = session.token
    except IndexError:
        token = create_session(user.id)
    return token

def session_lookup(token):
    try:
        session = session_store.get_one_by(token=token)
        user_id = session.user_id
    except IndexError:
        user_id = None
    return user_id

def login(username, password):
    if authenticate(username, password):
        return get_or_create_session(username)
    raise errors.WrapperException(errors.auth_failed, '')

def logout(token):
    try:
        session = session_store.get_one_by(token=token)
        session.delete()
    except Exception, err:
        print err



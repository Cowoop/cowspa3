import be.repository.access as dbaccess
import commonlib.helpers as helpers

def authenticate(username, password):
    encrypted = helpers.encrypt(password)
    passphrase = dbaccess.get_passphrase_by_username(username)
    return encrypted == passphrase

import commontest
import test_data
import be.repository.access as dbaccess
import be.apis.role as rolelib
import be.apis.user as userlib
from nose.tools import nottest

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()
 
def test_create_superuser():
    user_id = userlib.create_superuser(**test_data.super_user)
    assert rolelib.get_user_roles(user_id)['global'] == ["Admin"] 

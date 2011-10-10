import commontest
import test_data
import be.apis.system as systemlib
import be.apis.role as rolelib

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_setup():
    system_id, admin_id = systemlib.setup(**test_data.admin_user)
    env.context.pgcursor.connection.commit()
    assert system_id != admin_id
    assert type(system_id) == type(admin_id)
    assert type(system_id) in (int, long)
    assert admin_id > system_id
    # TODO: Important that below assrt works
    # assert rolelib.get_user_roles(admin_id)['global'] == ["Admin"]

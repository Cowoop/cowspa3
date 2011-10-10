import commontest
import test_data
import be.repository.access as dbaccess
import be.apis.role as rolelib
import be.apis.user as userlib
from nose.tools import nottest

# dependencies member
role_data = dict(context = 'BizPlace:1', roles = ['director', 'host'], user_id = 1)
role_map = dict(director='Director', host='Host')

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_assign_role():
    rolelib.assign(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).issubset(roles_dict[test_data.bizplace['name']]) == True
    env.context.pgcursor.connection.commit()

def test_reassign_role():
    rolelib.assign(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).issubset(roles_dict[test_data.bizplace['name']]) == True
    env.context.pgcursor.connection.commit()

def test_revoke_role():
    rolelib.revoke(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).intersection(roles_dict[test_data.bizplace['name']]) == set()
    env.context.pgcursor.connection.commit()

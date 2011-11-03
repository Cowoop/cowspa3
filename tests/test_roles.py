import commontest
import test_data
import be.apis.role as rolelib
from nose.tools import nottest

# dependencies member
role_data = dict(context = test_data.bizplace_id, roles = ['director', 'host'])
role_map = dict(director='Director', host='Host')

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_assign_role():
    role_data['user_id'] = test_data.member_id
    rolelib.assign(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).issubset(roles_dict[test_data.bizplace['name']]) == True
    env.context.pgcursor.connection.commit()

def test_reassign_role():
    role_data['user_id'] = test_data.member_id
    rolelib.assign(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).issubset(roles_dict[test_data.bizplace['name']]) == True
    env.context.pgcursor.connection.commit()

def test_revoke_role():
    role_data['user_id'] = test_data.member_id
    rolelib.revoke(**role_data)
    roles_dict = rolelib.get_user_roles(role_data['user_id'])
    assert set(role_map.values()).intersection(roles_dict[test_data.bizplace['name']]) == set()
    env.context.pgcursor.connection.commit()

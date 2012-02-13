import commontest
import test_data
import be.apis.role as rolelib
from nose.tools import nottest

# dependencies member
role_map = dict(director='Director', host='Host')

def get_role_data():
    return dict(context = test_data.bizplace_id, roles = ['director', 'host'], user_id=test_data.member_id)

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_assign_role():
    role_data = get_role_data()
    rolelib.new_roles(**role_data)
    for role_dict in rolelib.get_roles(role_data['user_id']):
        if role_dict['context'] == role_data['context']:
            break
    assert set(role_data['roles']).issubset([role['role'] for role in role_dict['roles']]) == True
    env.context.pgcursor.connection.commit()

def test_reassign_role():
    role_data = get_role_data()
    rolelib.new_roles(**role_data)
    assert set(role_data['roles']).issubset(rolelib.get_roles_in_context(role_data['user_id'], role_data['context'])) == True
    env.context.pgcursor.connection.commit()

def test_revoke_role():
    role_data = get_role_data()
    role_data['roles'] = []
    old_roles = rolelib.get_roles_in_context(role_data['user_id'], role_data['context'])
    rolelib.new_roles(**role_data)
    new_roles = rolelib.get_roles_in_context(role_data['user_id'], role_data['context'])
    assert set(new_roles).intersection(old_roles) == set()
    env.context.pgcursor.connection.commit()

import commontest
import test_data
import be.apis.user as userlib
import be.apis.role as rolelib
import commonlib.shared.roles as roledefs

#dependency member, BizPlace

def setup():
    commontest.setup_test_env()
    env.context.pgcursor.connection.commit()

def test_login():
    assert bool(userlib.login(test_data.member['username'], test_data.member['password'])) == True

def test_role_assign():
    member_id = test_data.member_id
    roles = ['host', 'director']
    rolelib.new_roles(member_id, roles, test_data.bizplace_id)
    env.context.pgcursor.connection.commit()

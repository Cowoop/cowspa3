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
    member_id = 1
    roles = ['host', 'director']
    rolelib.assign(member_id, roles, 'BizPlace:1')
    env.context.pgcursor.connection.commit()

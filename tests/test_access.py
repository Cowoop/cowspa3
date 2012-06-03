import test_data
import be.apis.role as rolelib
import be.apis.user as userlib
from be.libs.accesscontrol import *
from nose.tools import nottest

def test_role():
    userlib.set_context('kit', test_data.bizplace_id)
    condition = HAS_ROLES('host', test_data.bizplace_id)
    assert condition() == True
    condition = HAS_ROLES('host')
    assert condition() == True

def test_permissions():
    userlib.set_context('admin')
    condition = HAS_PERMS('admin')
    assert condition() == True
    assert NOT(condition)() == False

def test_access():
    userlib.set_context('bruba', test_data.bizplace_id)
    condition1 = HAS_ROLES('host', test_data.bizplace_id)
    assert condition1() == False
    condition2 = HAS_ROLES('member', test_data.bizplace_id)
    assert condition2() == True
    condition3 = ANY_ROLE(('host', 'member'), test_data.bizplace_id)
    assert condition3() == True
    condition4 = OR(condition1, condition2)
    assert condition4() == True
    condition5 = OR(condition2, condition1)
    assert condition5() == True
    condition6 = AND(condition2, condition1)
    assert condition6() == False

def test_authenticated():
    userlib.set_context('kit', test_data.bizplace_id)
    condition = Authenticated()
    assert condition() == True

import commontest
import commonlib.shared.states

States = commonlib.shared.states.states
class state(States):
    enabled = 0
    available = 1
    hidden = 2
    
def setup():
    commontest.setup_test_env()

def teardown():
    commontest.destroy_test_env()

def test_fromflags():
    state_flags = 5
    ob = state()
    state_dict = ob.to_dict(state_flags)
    print state_dict
    assert state_flags == ob.to_flags(state_dict)

def test_fromdict():
    state_dict = dict(enabled=False, available=True, hidden=False)
    ob = state()
    state_flags = ob.to_flags(state_dict)
    print state_flags
    assert state_dict == ob.to_dict(state_flags)

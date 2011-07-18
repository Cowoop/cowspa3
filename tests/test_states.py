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
    state_dict = state.to_dict(state_flags)
    assert state_flags == state.to_flags(state_dict)
    state_flags = 2
    assert state_flags != state.to_flags(state_dict)

def test_fromdict():
    state_dict = dict(enabled=False, available=True, hidden=False)
    state_flags = state.to_flags(state_dict)
    assert state_dict == state.to_dict(state_flags)
    state_dict['hidden'] = True
    assert state_dict != state.to_dict(state_flags)

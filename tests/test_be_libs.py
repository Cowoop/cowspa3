import commonlib.helpers
import commonlib.shared.constants
import be.libs.macros as macroslib
from be.libs.accesscontrol import AND, OR, NOT, Condition

class dummy_obj_state(commonlib.shared.constants.states):
    names = ["enabled", "available", "hidden"]
states = dummy_obj_state()

def add_a_b(context, data, macro_data):
    return str(data['a'] + data['b'])

def setup():
    macroslib.processors['add_a_b'] = add_a_b

def teardown():
    del macroslib.processors['add_a_b']

def test_macro_processing():
    text = 'A + B = {{add_a_b}}'
    data = dict(a=1, b=2)
    context = None
    assert macroslib.process(text, context, data) == 'A + B = 3'

def test_has_macro():
    text = 'HAS NO MACRO'
    assert macroslib.has_macro(text) == False

def test_constants():
    class Statuses(commonlib.helpers.Constants):
        names = ['open', 'pending', 'closed']

    statuses = Statuses()
    assert statuses.open == 0
    assert statuses.rev(0) == 'open'

def test_state():
    assert states.enabled == 1
    assert states.available == 2
    assert states.hidden == 4

def test_state_fromflags():
    state_flags = 5
    state_dict = states.to_dict(state_flags)
    assert state_flags == states.to_flags(state_dict)
    state_flags = 2
    assert state_flags != states.to_flags(state_dict)
    state_dict = states.to_dict(state_flags)
    assert not state_dict['enabled']
    assert state_dict['available']
    assert not state_dict['hidden']

def test_state_fromdict():
    state_dict = dict(enabled=False, available=True, hidden=False)
    state_flags = states.to_flags(state_dict)
    assert state_flags == 2
    assert state_dict == states.to_dict(state_flags)
    state_dict['hidden'] = True
    assert state_dict != states.to_dict(state_flags)
    assert states.to_flags(state_dict) == 6

def test_basic_access_clauses():

    class TRUE(Condition):
        def __call__(self):
            return True

    assert AND(TRUE(), TRUE())() == True
    assert OR(TRUE(), TRUE())() == True
    assert NOT(TRUE())() == False
    assert OR(TRUE(), NOT(TRUE()))() == True
    assert OR(NOT(TRUE()), NOT(TRUE()))() == False

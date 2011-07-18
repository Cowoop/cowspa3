import commonlib.shared.states
import be.libs.macros as macroslib

class dummy_obj_state(commonlib.shared.states.states):
    enabled = 0
    available = 1
    hidden = 2

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

def test_fromflags():
    state_flags = 5
    state_dict = dummy_obj_state.to_dict(state_flags)
    assert state_flags == dummy_obj_state.to_flags(state_dict)
    state_flags = 2
    assert state_flags != dummy_obj_state.to_flags(state_dict)

def test_fromdict():
    state_dict = dict(enabled=False, available=True, hidden=False)
    state_flags = dummy_obj_state.to_flags(state_dict)
    assert state_dict == dummy_obj_state.to_dict(state_flags)
    state_dict['hidden'] = True
    assert state_dict != dummy_obj_state.to_dict(state_flags)

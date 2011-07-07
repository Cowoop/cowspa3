import be.libs.macros as macroslib

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

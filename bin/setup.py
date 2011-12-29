import sys
sys.path.insert(0, '.')
import be
import be.bootstrap
be.bootstrap.start('conf_test')
import be.apps

app = be.apps.cowspa

defaults = dict(username="admin", name='The Admin')

def not_empty_input(prompt):
    v = None
    while not(v):
        v = raw_input(prompt)
    return v

username = raw_input("Admin username [%(username)s]: " % defaults) or defaults['username']
email = not_empty_input("Email: ")
password = not_empty_input("Password: ")
name = raw_input("Name [%(name)s]: " % defaults) or defaults['name']

app.mapper['setup'](username, password, email, name)

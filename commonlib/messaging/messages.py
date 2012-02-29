import os.path
import copy
from jinja2 import Environment

tenv = Environment('<%', '%>', '${', '}', '%%')
template_path = 'commonlib/messaging/templates'

def render(content, data):
    return tenv.from_string(content).render(**data)

class MessageMeta(type):
    def __new__(cls, name, bases, dct):
        tmplname = dct['name']
        if tmplname:
            content = open(os.path.join(template_path, tmplname)).read()
            content_dict = dict()
            exec(content, {}, content_dict)
            dct['content_dict'] = content_dict
        return type.__new__(cls, name, bases, dct)

class Message(object):
    __metaclass__ = MessageMeta
    name = ''
    def __init__(self, macros_data={}, overrides={}):
        self.macros_data = macros_data
        self.overrides = overrides
        self.message_dict = copy.copy(self.content_dict)
    def build(self):
        self.message_dict.update(self.overrides)
        for k,v in self.message_dict.items():
            if v is None:
                continue
            if isinstance(v, (list, tuple)):
                v = tuple(render(s, self.macros_data) for s in v)
            else:
                v = render(v, self.macros_data)
            self.message_dict[k] = v
    def email(self):
        return env.mailer.send(**self.message_dict)

class Activation(Message):
    name = 'activation'
class Invitation(Message):
    name = 'invitation'
class Invoice(Message):
    name = 'invoice'
class Booking(Message):
    name = 'booking'

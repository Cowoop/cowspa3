import inspect
import be.repository.access as dbaccess

member_store = dbaccess.stores.member_store

class BaseEvent(object):
    name = "base"
    category = ""
    def __init__(self, actor, created, data):
        self.created = created
        self.actor = actor
        self.data = data
    @property
    def msg_tmpl(self):
        return self._msg_tmpl()
    @property
    def tags(self):
        return self._tags()
    @property
    def message(self):
        data = self.data
        data.update(created=self.created, actor=self.actor)
        return self.msg_tmpl % data
    @property
    def access(self):
        return self._access()
    def _tags(self):
        return []
    def _msg_tmpl(self):
        return ''
    def _access(self):
        return []

class MemberCreated(BaseEvent):
    name = "member_created"
    category = "member_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " New member <a href='./profile?id=%(id)s#about'>%(name)s</a> created by %(actor_name)s."
    def _access(self):
        return ['global::admin', member_store.ref(self.actor)]

class MemberUpdated(BaseEvent):
    name = "member_updated"
    category = "member_management"
    def _msg_tmpl(self):
        if self.actor == self.data['id']:
            tmpl = "You have updated profile."
        else:
            tmpl = "%(actor_name)s has updated %(name)s's profile."
        return tmpl
    def _access(self):
        if self.actor  == self.data['id']:
            access = [member_store.ref(self.actor)]
        else:
            access = [member_store.ref(self.actor), member_store.ref(self.data['id'])]
        return access

class MemberDeleted(BaseEvent):
    name = "member_deleted"
    category = "member_management"
    def _msg_tmpl(self):
        return "%(name)s account is removed by %(actor_name)s."

class PasswordChanged(BaseEvent):
    name = "password_changed"
    category = "security"
    def _msg_tmpl(self):
        return "Password changed for %(name)s by %(actor_name)s."

class ResourceCreated(BaseEvent):
    name = "resource_created"
    category = "resource_management"
    msg_tmpl = "New resource %(name)s created by %(actor_name)s"

class Categories(dict):
    """
    subclassing dict to guarantee uniqueness of event name
    """
    def add_event(self, event):
        if not event.category in self:
            self[event.category] = {}
        elif event.name in self[event.category]:
            raise Exception("Event name not unique: " + event.name)
        self[event.category][event.name] = event
    def eventnames_for_role(self, roles):
        return tuple(itertools.chain(*(tuple(role_categories[role].values()) for role in roles)))

all_events = [o for o in globals().values() if inspect.isclass(o) and issubclass(o, BaseEvent)]
categories = Categories()

for event in all_events:
    if inspect.isclass(event) and issubclass(event, BaseEvent):
        categories.add_event(event)

role_categories = dict(
    admin = dict(
        member_management = ['member_created', 'member_updated'],
        security = [],
        resource_management = ['resource_created'] ),
    host = dict(
        member_management = ['member_created', 'member_updated'],
        security = [],
        resource_management = ['resource_created'] ),
    member = dict(
        member_management = ['member_updated'],
        security = ['password_changed'])
    )


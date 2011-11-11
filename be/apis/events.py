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
        return ['0:admin', self.actor]

class MemberInvited(BaseEvent):
    name = "member_invited"
    category = "member_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + ' %(actor_name)s has send membership invitaion to "%(first_name)s %(last_name)s"'
    def _access(self):
        return ['0:admin', self.actor]

class MemberUpdated(BaseEvent):
    name = "member_updated"
    category = "member_management"
    def _msg_tmpl(self):
        if self.actor == self.data['id']:
            tmpl = "You have updated profile."
        else:
            tmpl = "%(actor_name)s has updated %(name)s's profile."
        created_date = "<c class='date'>%s</c> " % self.data['created'].strftime('%b %-d, %Y')
        return created_date + tmpl
    def _access(self):
        if self.actor  == self.data['id']:
            access = [self.actor]
        else:
            access = [self.actor, self.data['id']]
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

class BizplaceCreated(BaseEvent):
    name = "bizplace_created"
    category = "bizplace_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " New place %(name)s created by %(actor_name)s."
    def _access(self):
        return ['0:admin', self.actor]

class BizplaceUpdated(BaseEvent):
    name = "bizplace_updated"
    category = "bizplace_management"
    def _msg_tmpl(self):
        if self.actor == self.data['id']:
            tmpl = "You have updated %(name)s place's profile."
        else:
            tmpl = "%(actor_name)s has updated %(name)s place's profile."
        return tmpl
    def _access(self):
        if self.actor  == self.data['id']:
            access = [self.actor]
        else:
            access = [self.actor, self.data['id']]
        return access

class ResourceCreated(BaseEvent):
    name = "resource_created"
    category = "resource_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " New resource (%(type)s) %(name)s created by %(actor_name)s for %(bizplace)s."
    def _access(self):
        return ['0:admin', self.actor]

class InvoiceCreated(BaseEvent):
    name = "invoice_created"
    category = "invoice_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " Invoice No.<a href='/invoice/%(invoice_id)s/html'>%(invoice_id)s</a> issued for <a href='./profile?id=%(member_id)s#about'>%(name)s</a> by %(actor_name)s."
    def _access(self):
        return ['0:admin', self.actor]
        
class InvoiceprefUpdated(BaseEvent):
    name = "invoicepref_updated"
    category = "invoicepref_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " Invoice Preferences %(attrs)s updated for Place %(name)s by %(actor_name)s."
    def _access(self):
        return ['0:admin', self.actor]
        
class BillingprefUpdated(BaseEvent):
    name = "billingpref_updated"
    category = "billingpref_management"
    def _msg_tmpl(self):
        created_date = "<c class='date'>%s</c>" % self.data['created'].strftime('%b %-d, %Y')
        return created_date + " Billing Preferences updated for <a href='./profile?id=%(member_id)s#about'>%(name)s</a> by %(actor_name)s."
    def _access(self):
        return ['0:admin', self.actor]
        
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
        bizplace_management = ['bizplace_created', 'bizplace_updated'],
        security = [],
        resource_management = ['resource_created'] ),
    host = dict(
        member_management = ['member_created', 'member_updated'],
        bizplace_management = ['bizplace_created'],
        security = [],
        resource_management = ['resource_created'] ),
    member = dict(
        member_management = ['member_updated'],
        security = ['password_changed'])
    )



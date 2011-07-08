import be.repository.stores as stores_mod
import bases.persistence

user_store = stores_mod.User()
contact_store = stores_mod.Contact()
member_store = stores_mod.Member()
memberpref_store = stores_mod.MemberPref()
memberprofile_store = stores_mod.MemberProfile()
registered_store = stores_mod.Registered()
session_store = stores_mod.Session()
permission_store = stores_mod.Permission()
role_store = stores_mod.Role()
user_perms_store = stores_mod.UserPermission()
user_roles_store = stores_mod.UserRole()
biz_store = stores_mod.Biz()
bizplace_store = stores_mod.BizPlace()
bizprofile_store = stores_mod.BizProfile()
bizplaceprofile_store = stores_mod.BizplaceProfile()
request_store = stores_mod.Request()
plan_store = stores_mod.Plan()
subscription_store = stores_mod.Subscription()
resource_store = stores_mod.Resource()
usage_store = stores_mod.Usage()
invoice_store = stores_mod.Invoice()
pricing_store = stores_mod.Pricing()
price_store = stores_mod.Price()
#activity_store = stores_mod.activity_store()

class RStore(object): pass

def make_rstore(store):
    rstore = RStore()
    for attr in ('ref', 'setup', 'add', 'remove', 'get', 'get_by', 'get_one_by'):
        method = getattr(store, attr)
        setattr(rstore, attr, method)
    return rstore

class stores: pass

for name, store in stores_mod.known_stores.items():
    setattr(stores, name, make_rstore(store))

# objects

class PObject(object):
    store = None
    attributes = []

    def __init__(self, oid):
        self.oid = oid
        self.attributes = tuple(self.store.schema.keys())

    def __getattr__(self, name):
        if name in self.attributes:
            return self.store.get(self.oid, [name], hashrows=False)[0]
        return object.__getattribute__(self, name)

    def __setattr__(self, name, v):
        if name in self.attributes:
            self.store.update(self.id, **{name:v})
        object.__setattr__(self, name, v)

    def update(self, **mod_data):
        self.store.update(self.id, **mod_data)

class Member(PObject):
    store = member_store
    @property
    def profile(self):
        return memberprofile_store.get_one_by(crit={'member':self.id})
    @profile.setter
    def profile(self, mod_data):
        memberprofile_store.update_by(crit={'member':self.id}, **mod_data)
    @property
    def contact(self):
        return contact_store.get_one_by(member=id)
    @contact.setter
    def contact(self, mod_data):
        ref = member_store.ref(self.id)
        contact_store.update_by(crit={'owner':ref}, mod_data=mod_data)
    @property
    def pref(self):
        return memberpref_store.get_one_by(member=self.id)
    @pref.setter
    def pref(self, mod_data):
        return memberpref_store.update_by(crit={'member':self.id}, **mod_data)
    def info(self):
        q = 'SELECT member_profile.member, member.state, member_profile.display_name from member_profile \
             INNER JOIN member ON member_profile.member = member.id WHERE member.id = %s'
        values = (self.id,)
        return user_store.query_exec(q, values)[0]
    def memberships(self):
        return subscription_store.get_by(crit=dict(subscriber_id=self.id))

class Biz(PObject):
    store = biz_store
    def info(self):
        ref = biz_store.ref(self.id)
        q = 'SELECT biz.name, biz.state, \
             bizprofile.short_description, bizprofile.tags, bizprofile.website, bizprofile.blog, \
             contact.address, contact.city, contact.country, contact.email \
             from biz \
             INNER JOIN contact ON contact.owner = %(ref)s \
             INNER JOIN bizprofile ON bizprofile.biz = %(biz_id)s \
             WHERE biz.id = %(biz_id)s'
        values = dict(biz_id=self.id, ref=ref)
        return biz_store.query_exec(q, values)[0]

class BizPlace(PObject):
    store = bizplace_store
    info_sql = 'SELECT bizplace.name, bizplace.state, \
        bizplaceprofile.short_description, bizplaceprofile.tags, bizplaceprofile.website, bizplaceprofile.blog, \
        contact.address, contact.city, contact.country, contact.email \
        from bizplace '

    def info(self):
        ref = bizplace_store.ref(self.id)
        q = self.info_sql + \
        """
        INNER JOIN contact ON contact.owner = %(ref)s
        INNER JOIN bizplaceprofile ON bizplaceprofile.bizplace = %(bizplace_id)s
        WHERE bizplace.id = %(bizplace_id)s
        """
        values = dict(bizplace_id=self.id, ref=ref)
        return bizplace_store.query_exec(q, values)[0]


class Subscription(object): pass
class Contact(object): pass
class Plan(object): pass
class Resource(object): pass
class Usage(object): pass
class Invoice(object): pass

# functions

def get_passphrase_by_username(username):
    return user_store.get_by(crit={'username': username})[0].password

def add_membership(member_id, plan_id):
    plan = plan_store.get(plan_id)
    bizplace_name = bizplace_store.get(bizplace_id, fields=['name']).name
    data = dict(plan_id=plan_id, subscriber_id=member_id, plan_name=plan.name, bizplace_id=plan.bizplace_id, bizplace_name=bizplace_name)
    subscription_store.add(**data)
    return True

def find_bizplace_members(bizplace_ids, fields=['member', 'display_name']):
    bizplace_ids = tuple(bizplace_ids)
    clause = 'member IN (SELECT subscriber_id FROM subscription WHERE bizplace_id IN %s)'
    clause_values = (bizplace_ids,)
    return memberprofile_store.get_by_clause(clause, clause_values, fields)

def list_bizplaces():
    q = BizPlace.info_sql
    q += """
    INNER JOIN contact ON contact.owner = 'BizPlace:' || bizplace.id
    INNER JOIN bizplaceprofile ON bizplaceprofile.bizplace = bizplace.id
    """
    return bizplace_store.query_exec(q)

def find_plan_members(plan_ids, fields=['member', 'display_name']):
    plan_ids = tuple(plan_ids)
    clause = 'member IN (SELECT subscriber_id FROM subscription WHERE plan_id IN %s)'
    clause_values = (plan_ids,)
    return memberprofile_store.get_by_clause(clause, clause_values, fields)

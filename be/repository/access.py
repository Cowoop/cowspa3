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
    for attr in ('ref', 'setup', 'add', 'remove'):
        method = getattr(store, attr)
        setattr(rstore, attr, method)
    return rstore

class stores: pass

for name, store in stores_mod.known_stores.items():
    setattr(stores, name, make_rstore(store))

class PObject(object):
    def __init__(self, id):
        self.id = id

class Member(PObject):
    @property
    def profile(self):
        return memberprofile_store.get_one_by(member=self.id)
    @profile.setter
    def profile(self, mod_data):
        profilestore.update_by(crit={'member':self.id}, **mod_data)
    @property
    def contact(self):
        return contactstore.get_one_by(member=id)
    @contact.setter
    def contact(self, mod_data):
        ref = memberstore.ref(self.id)
        contactstore.update_by(crit={'owner':ref}, mod_data=mod_data)
    @property
    def pref(self):
        return memberpref_store.get_one_by(member=self.id)
    @pref.setter
    def pref(self, mod_data):
        return memberpref_store.update_by(crit={'member':self.id}, **mod_data)

class Contact(object): pass
class Biz(object): pass
class BizPlace(object): pass
class Plan(object): pass
class Resource(object): pass
class Usage(object): pass
class Invoice(object): pass

# functions


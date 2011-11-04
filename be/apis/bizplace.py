import datetime
import be.repository.access as dbaccess
import be.apis.role as rolelib
import be.apis.activities as activitylib
import be.apis.invoicepref as invoicepreflib
import commonlib.shared.static as static

bizplace_store = dbaccess.stores.bizplace_store

class BizplaceCollection:
    def new(self, name, address, city, country, email, short_description, long_description=None, tags=None, website=None, blog=None, twitter=None, facebook=None, linkedin=None, phone=None, fax=None, sip=None, skype=None, mobile=None, currency=None):
        created = datetime.datetime.now()
        bizplace_id = dbaccess.OidGenerator.next("BizPlace")
        data = dict(id=bizplace_id, name=name, created=created, short_description=short_description, long_description=long_description, tags=tags, website=website, blog=blog, twitter=twitter, facebook=facebook, address=address, city=city, country=country, email=email, phone=phone, fax=fax, sip=sip, skype=skype, mobile=mobile, currency=currency)
        bizplace_store.add(**data)

        rolelib.new_roles(user_id=env.context.user_id, roles=['director', 'host'], context=bizplace_id)

        invoicepreflib.invoicepref_collection.new(**dict(owner=bizplace_id))

        data = dict(name=name, id=bizplace_id)
        activity_id = activitylib.add('bizplace_management', 'bizplace_created', data, created)

        return bizplace_id

    def list(self, owner=None):
        """
        returns list of bizplace info dicts
        """
        if not owner:
            owner = env.context.user_id
            roles = env.context.roles
        else:
            roles = rolelib.get_roles(owner, ['host', 'director', 'admin'])
        ids = [role for context, role in roles if context]
        return dbaccess.list_bizplaces(ids)

    def all(self):
        """
        returns list of all bizplace info dicts
        """
        return dbaccess.list_all_bizplaces()

    def members(self, bizplace_id, show_enabled=True, show_disabled=True, show_hidden=True):
        """
        returns list bizplace members in the form of tuple (id, display_name)
        """
        return dbaccess.find_bizplace_members(bizplace_id)

class BizplaceResource:

    get_attributes = ['taxes', 'default_plan']
    set_attributes = ['taxes', 'default_plan']

    def info(self, bizplace_id):
        """
        returns dict containing essential information of specified business place
        """
        return dbaccess.bizplace_info(bizplace_id)

    def plans(self, bizplace_id):
        """
        returns list of plan info dicts for this business place
        """
        return dbaccess.find_bizplace_plans(bizplace_id, dbaccess.plan_info_fields)

    def update(self, bizplace_id, **mod_data):
        bizplace_store.update(bizplace_id, **mod_data)
        
        bizplace_name = bizplace_store.get(bizplace_id, fields=['name'])
        data = dict(id=bizplace_id, name=bizplace_name, attrs=', '.join(attr for attr in mod_data))
        activity_id = activitylib.add('bizplace_management', 'bizplace_updated', data)


    def get(self, bizplace_id, attrname):
        if not attrname in self.get_attributes: return
        return bizplace_store.get(bizplace_id, fields=[attrname])

    def set(self, bizplace_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(bizplace_id, **{attrname: v})

bizplace_collection = BizplaceCollection()
bizplace_resource = BizplaceResource()

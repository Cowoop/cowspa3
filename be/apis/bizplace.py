import datetime
import be.repository.access as dbaccess

biz_store = dbaccess.biz_store
bizplace_store = dbaccess.bizplace_store

class BizplaceCollection:
    def new(self, biz_id, name, address, city, country, email, short_description, long_description=None, tags=None, website=None, blog=None, twitter=None, facebook=None, linkedin=None, phone=None, fax=None, sip=None, skype=None, mobile=None):
        created = datetime.datetime.now()
        data = dict(biz=biz_id, name=name, created=created, short_description=short_description, long_description=long_description, tags=tags, website=website, blog=blog, twitter=twitter, facebook=facebook, address=address, city=city, country=country, email=email, phone=phone, fax=fax, sip=sip, skype=skype, mobile=mobile)
        bizplace_id = bizplace_store.add(**data)
        bizplace_ref = bizplace_store.ref(bizplace_id)

        return bizplace_id

    def list(self):
        """
        returns list of bizplace info dicts
        """
        return dbaccess.list_bizplaces()


    def members(self, bizplace_id, show_enabled=True, show_disabled=True, show_hidden=True):
        """
        returns list bizplace members in the form of tuple (id, display_name)
        """
        return dbaccess.find_bizplace_members(bizplace_id)

class BizplaceResource:

    get_attributes = ['taxes']
    set_attributes = ['taxes']

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

    def get(self, bizplace_id, attrname):
        if not attrname in self.get_attributes: return
        return bizplace_store.get(bizplace_id, fields=[attrname])

    def set(self, bizplace_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(bizplace_id, **{attrname: v})

bizplace_collection = BizplaceCollection()
bizplace_resource = BizplaceResource()

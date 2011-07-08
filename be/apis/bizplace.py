import datetime
import be.repository.access as dbaccess

biz_store = dbaccess.biz_store
contact_store = dbaccess.stores.contact_store
bizprofile_store = dbaccess.stores.bizprofile_store
bizplace_store = dbaccess.bizplace_store
bizplaceprofile_store = dbaccess.stores.bizplaceprofile_store

class BizplaceCollection:
    def new(self, biz_id, name, address, city, country, email, short_description, long_description=None, tags=None, website=None, blog=None, twitter=None, facebook=None, linkedin=None, phone=None, fax=None, sip=None, skype=None, mobile=None):
        created = datetime.datetime.now()
        data = dict(biz=biz_id, name=name, created=created)
        bizplace_id = bizplace_store.add(**data)
        bizplace_ref = bizplace_store.ref(bizplace_id)

        data = dict(owner=bizplace_ref, address=address, city=city, country=country, email=email, phone=phone, fax=fax, sip=sip, skype=skype, mobile=mobile)
        contact_store.add(**data)

        data = dict(bizplace=bizplace_id, short_description=short_description, long_description=long_description, tags=tags, website=website, blog=blog, twitter=twitter, facebook=facebook)
        bizplaceprofile_store.add(**data)

        return bizplace_id

    def list(self):
        """
        returns list of bizplace info dicts
        """
        return dbaccess.list_bizplaces()


    def members(self, bizplace_id, show_enabled=True, show_disabled=True, show_hidden=True):
        """
        returns list bizplace members
        """

class BizplaceResource:

    def info(self, bizplace_id):
        """
        returns dict containing essential information of specified business place
        """
        return dbaccess.BizPlace(bizplace_id).info()

    def plans(self, bizplace_id):
        """
        returns list of plan info dicts for this business place
        """

bizplace_collection = BizplaceCollection()
bizplace_resource = BizplaceResource()

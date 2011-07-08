import datetime
import be.repository.access as dbaccess

biz_store = dbaccess.biz_store
contact_store = dbaccess.stores.contact_store
bizprofile_store = dbaccess.stores.bizprofile_store
bizplace_store = dbaccess.bizplace_store
bizplaceprofile_store = dbaccess.stores.bizplaceprofile_store

class BizCollection:

    def new(self, name, address, city, country, email, short_description, long_description=None, tags=None, website=None, blog=None, twitter=None, facebook=None, linkedin=None, phone=None, fax=None, sip=None, skype=None, mobile=None):
        created = datetime.datetime.now()
        data = dict(name=name, created=created)
        biz_id = biz_store.add(**data)
        biz_ref = biz_store.ref(biz_id)

        data = dict(owner=biz_ref, address=address, city=city, country=country, email=email, phone=phone, fax=fax, sip=sip, skype=skype, mobile=mobile)
        contact_store.add(**data)

        data = dict(biz=biz_id, short_description=short_description, long_description=long_description, tags=tags, website=website, blog=blog, twitter=twitter, facebook=facebook)
        bizprofile_store.add(**data)

        return biz_id

    def list(self, ):
        """
        returns list of bizplace info dicts
        """

class BizResource:

    def info(self, biz_id):
        """
        returns dict containing essential information of specified business
        """
        return dbaccess.Biz(biz_id).info()

    def update(self, biz_id, mod_data):
        """
        """

    def bizplaces(self, biz_id):
        """
        """

biz_resource = BizResource()
biz_collection = BizCollection()

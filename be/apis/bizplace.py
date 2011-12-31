import datetime
import be.repository.access as dbaccess
import be.apis.role as rolelib
import be.apis.activities as activitylib
import be.apis.invoicepref as invoicepreflib
import be.apis.resource as resourcelib
import commonlib.shared.static as static
from babel.numbers import get_currency_symbol, get_decimal_symbol, get_group_symbol

bizplace_store = dbaccess.stores.bizplace_store

class BizplaceCollection:
    def new(self, name, address, city, country, email, short_description,
            long_description=None, tags=None, website=None, blog=None,
            twitter=None, facebook=None, linkedin=None, phone=None, fax=None,
            skype=None, mobile=None, currency=None, host_email=None,
            booking_email=None, tz='UTC'):
        created = datetime.datetime.now()
        bizplace_id = dbaccess.OidGenerator.next("BizPlace")
        data = dict(id=bizplace_id, name=name, created=created,
                short_description=short_description,
                long_description=long_description, tags=tags, website=website,
                blog=blog, twitter=twitter, facebook=facebook, address=address,
                city=city, country=country, email=email, phone=phone, fax=fax,
                skype=skype, mobile=mobile, currency=currency,
                host_email=host_email, booking_email=booking_email, tz=tz)
        bizplace_store.add(**data)

        rolelib.new_roles(user_id=env.context.user_id, roles=['director', 'host'], context=bizplace_id)
        start_number = dbaccess.generate_invoice_start_number()
        invoicepreflib.invoicepref_collection.new(**dict(owner=bizplace_id, start_number=start_number))
        default_tariff_id = resourcelib.resource_collection.new_tariff('Guest Tariff', 'Guest Tariff', bizplace_id, 0)
        bizplace_store.update(bizplace_id, default_tariff=default_tariff_id)

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
            roles = dbaccess.userrole_store.get_by(dict(user_id=owner), ['context',  'role'], False)
        my_bizplace_ids = set(context for context, role in roles if context)
        result = dbaccess.list_bizplaces(my_bizplace_ids)
        #DB returns country numeric code, which needs to be replaced by label
        #before it is returned
        for rec in result:
            rec['country'] = static.countries_map[rec['country']]

        return result


    def all(self):
        """
        returns list of all bizplace info dicts
        """
        result = dbaccess.list_all_bizplaces()
        #DB returns country numeric code, which needs to be replaced by label
        #before it is returned
        for rec in result :
            rec['country'] = static.countries_map[rec['country']]

        return result

    def members(self, bizplace_id, show_enabled=True, show_disabled=True, show_hidden=True):
        """
        returns list bizplace members in the form of tuple (id, name)
        """
        return dbaccess.find_bizplace_members(bizplace_id)

class BizplaceResource:

    get_attributes = ['name', 'city', 'email', 'default_tariff']
    set_attributes = ['name', 'city', 'email', 'default_tariff']

    def info(self, bizplace_id):
        """
        returns dict containing essential information of specified business place
        """
        result = dbaccess.bizplace_info(bizplace_id)

        #DB returns country numeric code, which needs to be replaced by label
        #before it is returned
        result['country'] = static.countries_map[result['country']]

        return result


    def plans(self, bizplace_id):
        """
        returns list of plan info dicts for this business place
        """
        return dbaccess.find_bizplace_plans(bizplace_id, dbaccess.tariff_info_fields)

    #TODO: dictshield to validate mod_data especially taxes
    def update(self, bizplace_id, **mod_data):
        bizplace_store.update(bizplace_id, **mod_data)

        bizplace_name = bizplace_store.get(bizplace_id, fields=['name'])
        data = dict(id=bizplace_id, name=bizplace_name, attrs=', '.join(attr for attr in mod_data))
        activity_id = activitylib.add('bizplace_management', 'bizplace_updated', data)

    def currency(self,bizplace_id,user_id):
        symbol=get_currency_symbol(bizplace_store.get(bizplace_id,fields=['currency']))
        user_locale = dbaccess.stores.memberpref_store.get_by(dict(member=user_id), ['language'])[0]['language']
        decimal=get_decimal_symbol(user_locale)
        group=get_group_symbol(user_locale)
        return dict(symbol=symbol, decimal=decimal, group=group)

    def get(self, bizplace_id, attrname):
        if not attrname in self.get_attributes: return
        return bizplace_store.get(bizplace_id, fields=[attrname])

    def set(self, bizplace_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(bizplace_id, **{attrname: v})

bizplace_collection = BizplaceCollection()
bizplace_resource = BizplaceResource()

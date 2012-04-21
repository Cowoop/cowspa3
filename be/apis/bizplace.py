import datetime
import be.repository.access as dbaccess
import be.apis.role as rolelib
import be.apis.activities as activitylib
import be.apis.member as memberlib
import be.apis.resource as resourcelib
import be.apis.usage as usagelib
import commonlib.shared.static as static
import be.apis.invoicepref as invoicepreflib
from babel.numbers import get_currency_symbol, get_decimal_symbol, get_group_symbol

bizplace_store = dbaccess.stores.bizplace_store

class BizplaceCollection:
    def new(self, name, address, city, country, email, short_description, province=None, long_description=None, tags=None, website=None,
        blog=None, twitter=None, facebook=None, linkedin=None, phone=None, fax=None, skype=None, mobile=None, currency='USD',
        host_email=None, booking_email=None, tz='UTC', skip_default_tariff=False, add_dummy_data=False):

        created = datetime.datetime.now()
        bizplace_id = dbaccess.OidGenerator.next("BizPlace")
        data = dict(id=bizplace_id, name=name, created=created,
                short_description=short_description,
                long_description=long_description, tags=tags, website=website,
                blog=blog, twitter=twitter, facebook=facebook, address=address,
                city=city, country=country, email=email, phone=phone, fax=fax,
                skype=skype, mobile=mobile, currency=currency, province=province,
                host_email=host_email, booking_email=booking_email, tz=tz)
        bizplace_store.add(**data)

        rolelib.new_roles(user_id=env.context.user_id, roles=['director', 'host'], context=bizplace_id)

        start_number=dbaccess.generate_invoice_start_number()
        invoicepreflib.invoicepref_collection.new(**dict(owner=bizplace_id, start_number=start_number))

        if not skip_default_tariff: # migration specific code. don't use skip_default_tariff otherwise
            default_tariff_id = resourcelib.resource_collection.new_tariff('Guest Tariff', 'Guest Tariff', bizplace_id, 0)
            bizplace_store.update(bizplace_id, default_tariff=default_tariff_id)

        data = dict(name=name, id=bizplace_id)
        activity_id = activitylib.add('bizplace_management', 'bizplace_created', data, created)

        if add_dummy_data:
# name, short_description, type, owner, default_price=None, enabled=True, calendar=False, host_only=False, long_description=None, calc_mode=CalcMode.monthly
            resource_id = resourcelib.resource_collection.new(name="Sunshine Room (Sample)", short_description="Room with nice windows. Can accomodate twenty people. _Sample resource_", type="room", owner=bizplace_id, default_price=100, calendar=True, calc_mode=resourcelib.CalcMode.time_based)
            # Sample usage 1
            now = datetime.datetime.now()
            start_time = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
            end_time = datetime.datetime(now.year, now.month, now.day, 12, 0, 0)
            usagelib.usage_collection.new(resource_id=resource_id, resource_name="Sunshin Room (Sample)", resource_owner=bizplace_id, member=env.context.user_id, start_time=start_time, end_time=end_time)
            # Sample usage 2
            start_time = datetime.datetime(now.year, now.month, now.day, 12, 0, 0)
            end_time = datetime.datetime(now.year, now.month, now.day, 15, 0, 0)
            usagelib.usage_collection.new(resource_id=resource_id, resource_name="Sunshin Room (Sample)", resource_owner=bizplace_id, member=env.context.user_id, start_time=start_time, end_time=end_time)
            tariff_id = resourcelib.resource_collection.new_tariff(name="Starter Plan (Sample)", short_description="_Sample membership plan_ Great plan for startups", type="tariff", owner=bizplace_id, default_price=299)

        return bizplace_id

    def list(self, owner=None):
        """
        returns list of bizplace info dicts
        """
        if not owner:
            owner = env.context.user_id
            roles = env.context.roles
        else:
            roles = rolelib.get_roles(owner)
        my_bizplace_ids = set(role.context for role in roles if role.context)
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

    get_attributes = ['name', 'city', 'email', 'default_tariff', 'province']
    set_attributes = ['name', 'city', 'email', 'default_tariff', 'province']

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

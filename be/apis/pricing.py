import datetime
import bases.app as applib
import be.repository.access as dbaccess
import be.errors
import commonlib.helpers

resource_store = dbaccess.resource_store
pricing_store = dbaccess.pricing_store

def new(resource_id, tariff_id, starts, amount):
    # starts should be greater than last pricings start which has no 'ends' date yet
    starts = commonlib.helpers.iso2date(starts)
    old_pricings = pricing_store.get_by(crit=dict(plan=tariff_id, resource=resource_id, ends=None))
    if old_pricings:
        old_pricing = old_pricings[0]
        if old_pricing.starts >= starts:
            msg = "Pricing start date should be greater than %s" % starts
            raise be.errors.ErrorWithHint(msg)
        old_pricing_ends = starts - datetime.timedelta(1)
        pricing_resource.set(old_pricing.id, 'ends', old_pricing_ends)
    return pricing_store.add(plan=tariff_id, resource=resource_id, starts=starts, amount=amount)

def destroy(tariff_id):
    raise NotImplemented

def list(tariff_id, for_date):
    """
    returns list of pricings for the plan
    """
    raise NotImplemented

def list_for_resource(resource_id):
    """
    returns list of pricings for specified resource
    """
    raise NotImplemented

def get(member_id, resource_id, usage_time=None):
    # TODO: if resource owner is not bizplace then?
    if not usage_time:
        usage_time = datetime.datetime.now().isoformat()
    bizplace_id = resource_store.get(resource_id, fields=['owner'], hashrows=False)
    plan_id = dbaccess.get_member_plan_id(member_id, bizplace_id, usage_time)
    pricing = dbaccess.get_resource_pricing(plan_id, resource_id, usage_time)
    if pricing:
        return pricing[0].amount

pricings = applib.Collection()
pricings.new = new
pricings.get = get
pricings.list = list_for_resource

def info(pricing_id):
    result = pricing_store.get(pricing_id)
    result['starts'] = result['starts'].isoformat()
    result['ends'] = result['ends'].isoformat() if result['ends'] else result['ends']
    return result

def update(tariff_id, resource_prices):
    """
    resource_prices: a tuple containing resource_id, prices and date from which the pricing will be activated
    """
    raise NotImplemented

pricing = applib.Resource()
pricing.info = info
pricing.update = update

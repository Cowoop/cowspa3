import datetime
import bases.app as applib
import be.repository.access as dbaccess
import be.errors
import commonlib.helpers
import be.libs.cost as costlib

odict = commonlib.helpers.odict

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
        set(old_pricing.id, 'ends', old_pricing_ends)
    return pricing_store.add(plan=tariff_id, resource=resource_id, starts=starts, amount=amount)

def destroy(tariff_id):
    raise NotImplemented

def by_resource(resource_id, for_date=None):
    """
    returns list of pricings for specified resource
    """
    for_date = for_date or datetime.datetime.now()
    return dbaccess.get_resource_pricings(resource_id, for_date)

def lst(resource_id, tariff_id):
    return pricing_store.get_by(crit=dict(resource=resource_id, plan=tariff_id), fields=['id', 'starts', 'ends', 'amount'])


def get(member_id, resource_id, usage_time=None):
    # TODO: if resource owner is not bizplace then?
    if not usage_time:
        usage_time = datetime.datetime.now()
    bizplace_id = resource_store.get(resource_id, fields=['owner'], hashrows=False)
    plan_id = dbaccess.get_member_plan_id(member_id, bizplace_id, usage_time)
    pricing = dbaccess.get_resource_pricing(plan_id, resource_id, usage_time)
    if pricing:
        return pricing[0].amount

def member_tariff(member_id, bizplace_id, usage_time=None):
    if not usage_time:
        usage_time = datetime.datetime.now()
    tariff_id = dbaccess.get_member_plan_id(member_id, bizplace_id, usage_time)
    return dbaccess.get_tariff_pricings(tariff_id, usage_time)

pricings = applib.Collection()
pricings.new = new
pricings.get = get
pricings.list = lst
pricings.by_resource = by_resource

settable_attrs = ['starts', 'ends', 'cost']

def info(pricing_id):
    return pricing_store.get(pricing_id)

def set(pricing_id, attr, value):
    if attr not in settable_attrs:
        return
    pricing_store.update(pricing_id, **{attr: value})

pricing = applib.Resource()
pricing.info = info
pricing.set = set

## Cost calculations

class InitialCost(costlib.Rule):
    name = 'Initial Cost'
    def apply(self, env, usage, cost):
        rate = pricings.get(usage.member_id, usage.resource_id, usage.starts)
        amount = rate * usage.quantity
        cost.new(self.name, amount)
        return costlib.flags.proceed

class Taxes(costlib.Rule):
    name = 'Initial Cost'
    def apply(self, env, usage, cost):
        raise NotImplemented

rules = [InitialCost()]

def calculate_cost(member_id, resource_id, quantity, starts, ends):
    usage = odict(member_id=member_id, resource_id=resource_id, quantity=quantity, starts=starts, ends=ends)
    resource = resource_store.get(usage.resource_id)
    if resource.time_based:
        quantity = (ends - starts).seconds / 3600.0
    processor = costlib.Processor(usage, rules)
    return processor.run()

import datetime
import bases.app as applib
import be.repository.access as dbaccess
import be.errors
import commonlib.helpers
import be.libs.cost as costlib
import be.libs.signals as signals
import calendar

odict = commonlib.helpers.odict

resource_store = dbaccess.resource_store
pricing_store = dbaccess.pricing_store

class CalcMode:

    quantity_based = 0
    time_based = 1
    monthly = 2

def new(resource_id, tariff_id, starts, amount, ends=None):

    old_pricing = dbaccess.get_resource_pricing(tariff_id, resource_id, starts)
    if starts and old_pricing:
        starts = commonlib.helpers.iso2date(starts)
        ends = old_pricing.ends
        if old_pricing.starts and old_pricing.starts>= starts:
            msg = "Pricing start date should be greater than %s" % old_pricing.starts
            raise be.errors.ErrorWithHint(msg)
        old_pricing_ends = starts - datetime.timedelta(1)
        set(old_pricing.id, 'ends', old_pricing_ends)
    return pricing_store.add(plan=tariff_id, resource=resource_id, starts=starts, ends=ends, amount=amount)

def destroy(tariff_id):
    raise NotImplemented

def by_resource(resource_id, for_date=None):
    """
    returns list of pricings for specified resource
    """
    for_date = for_date or datetime.datetime.now()
    return dbaccess.get_resource_pricings(resource_id, for_date)

def lst(resource_id, tariff_id):
    return pricing_store.get_by(crit=dict(resource=resource_id, plan=tariff_id), fields=['id', 'starts', 'ends', 'amount'], order_by="ends DESC")

def by_tariff(tariff_id):
    return pricing_store.get_by(crit=dict(plan=tariff_id))

def by_location(owner):
    """
    returns pricing for ALL the resources for each tariff defined for this
    location
    """

    default_tariff_id = dbaccess.bizplace_store.get(owner).default_tariff
    result = dbaccess.list_resources_and_tariffs(owner, ['id','name'], type='tariff')
    for rec in result:
        if rec['id'] == default_tariff_id :
            rec['is_guest_tariff'] = 1
        else:
            rec['is_guest_tariff'] = 0
        prices = pricing_store.get_by(crit=dict(plan=rec['id']), fields=['id','resource','amount'])
        price_per_resource = {}
        for p in prices :
            price_per_resource[p['resource']] = p
            del p['resource']
        rec['pricings'] = price_per_resource
    return result

def get(member_id, resource_id, usage_time=None):
    """
    returns rate
    """
    # TODO: if resource owner is not bizplace then?
    if not usage_time:
        usage_time = datetime.datetime.now()
    bizplace_id = resource_store.get(resource_id, fields=['owner'], hashrows=False)
    plan_id = dbaccess.get_member_plan_id(member_id, bizplace_id, usage_time)
    pricing = dbaccess.get_resource_pricing(plan_id, resource_id, usage_time)
    if pricing:
        return pricing.amount
    return dbaccess.get_default_pricing(resource_id, usage_time).amount

def member_tariff(member_id, bizplace_id, usage_time=None):
    if not usage_time:
        usage_time = datetime.datetime.now()
    tariff_id = dbaccess.get_member_plan_id(member_id, bizplace_id, usage_time)
    return dbaccess.get_tariff_pricings(tariff_id, usage_time)
    
def delete(pricing_id):
    pricing = pricing_store.get(pricing_id)
    if dbaccess.find_usage(start=pricing.starts, end=pricing.ends, resource_ids=[pricing.resource]):
        msg = "Usages are associated with this pricing, you can't delete pricing."
        raise be.errors.ErrorWithHint(msg)
    crit = dict(plan=pricing.plan, resource=pricing.resource, ends=pricing.starts-datetime.timedelta(1))
    prev_pricing = pricing_store.get_by(crit)[0]
    if prev_pricing: set(prev_pricing.id, 'ends', pricing.ends)
    return pricing_store.remove(pricing_id)
    
pricings = applib.Collection()
pricings.new = new
pricings.get = get
pricings.list = lst
pricings.by_resource = by_resource
pricings.by_tariff = by_tariff
pricings.by_location = by_location
pricings.delete = delete

settable_attrs = ['starts', 'ends', 'cost']

def info(pricing_id):
    return pricing_store.get(pricing_id)

def set(pricing_id, attr, value):    
    if attr not in settable_attrs:
        return
    pricing_store.update(pricing_id, **{attr: value})

def update(pricing_id, **mod_data):
    pricing = pricing_store.get(pricing_id)
    new_starts = commonlib.helpers.iso2date(mod_data['starts']) if 'starts' in mod_data else pricing.starts
    
    #Checking time interval for which pricing will change
    if pricing.starts == new_starts:
        changed_intervals_starts = pricing.starts
        changed_intervals_ends = pricing.ends  
    elif pricing.starts < new_starts:
        changed_intervals_starts = pricing.starts
        changed_intervals_ends = new_starts
    elif pricing.starts > new_starts:
        changed_intervals_starts = new_starts
        changed_intervals_ends = pricing.starts
    
    #Checking usages for pricing changed time interval
    if dbaccess.find_usage(start=changed_intervals_starts, end=changed_intervals_ends, resource_ids=[pricing.resource]):
        msg = "Usages are associated with this pricing, you can't delete pricing."
        raise be.errors.ErrorWithHint(msg)
        
    if new_starts != pricing.starts:
        mod_data['starts'] = new_starts
        crit = dict(plan=pricing.plan, resource=pricing.resource, ends=pricing.starts-datetime.timedelta(1))
        prev_pricing = pricing_store.get_by(crit)[0]
        if prev_pricing: set(prev_pricing.id, 'ends', pricing.ends)
        old_pricing = dbaccess.get_resource_pricing(pricing.plan, pricing.resource, new_starts, [pricing_id])
        if old_pricing:#old_pricing contains pricing at new_starts
            if old_pricing.starts and old_pricing.starts >= new_starts:
                msg = "Pricing start date should be greater than %s" % old_pricing.starts
                raise be.errors.ErrorWithHint(msg)
            mod_data['ends'] = old_pricing.ends
            set(old_pricing.id, 'ends', mod_data['starts']-datetime.timedelta(1))
    pricing_store.update(pricing_id, **mod_data)
    
pricing = applib.Resource()
pricing.info = info
pricing.set = set
pricing.update = update

## Cost calculations

class CustomResource(costlib.Rule):
    name = 'Custom Resource'
    def apply(self, env, usage, cost):
        if not usage.resource_id:
            assert usage.cost is not None, "Cost is mandatory for Custom Resource"
            cost.new(self.name, usage.cost)
            return costlib.flags.stop
        return costlib.flags.proceed

class InitialCost(costlib.Rule):
    name = 'Initial Cost'
    def apply(self, env, usage, cost):
        resource = resource_store.get(usage.resource_id)
        if resource.calc_mode == CalcMode.time_based:
            usage['quantity'] = (usage.ends - usage.starts).total_seconds() / 3600.0
        elif resource.calc_mode == CalcMode.monthly:
            usage['quantity'] = ((usage.ends - usage.starts).days + 1) / float(calendar.monthrange(usage.starts.year, usage.starts.month)[1])
        rate = float(pricings.get(usage.member_id, usage.resource_id, usage.starts))
        amount = rate * usage.quantity
        cost.new(self.name, costlib.to_decimal(amount))
        return costlib.flags.proceed

class Taxes(costlib.Rule):
    name = 'Initial Cost'
    def apply(self, env, usage, cost):
        raise NotImplemented

rules = [CustomResource(), InitialCost()]

def calculate_cost(member_id, resource_id, quantity, starts, ends=None, cost=None):
    starts = commonlib.helpers.iso2datetime(starts)
    ends = commonlib.helpers.iso2datetime(ends) if ends else starts
    usage = odict(member_id=member_id, resource_id=resource_id, quantity=quantity, starts=starts, ends=ends, cost=cost)
    processor = costlib.Processor(usage, rules)
    return processor.run()

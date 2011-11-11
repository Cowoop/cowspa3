import datetime
import be.repository.access as dbaccess
import be.errors
import commonlib.helpers

pricing_store = dbaccess.pricing_store

class PricingCollection:

    def new(self, resource_id, plan_id, starts, amount):
        # starts should be greater than last pricings start which has no 'ends' date yet
        starts = commonlib.helpers.iso2date(starts)
        old_pricings = pricing_store.get_by(crit=dict(plan=plan_id, resource=resource_id, ends=None))
        if old_pricings:
            old_pricing = old_pricings[0]
            if old_pricing.starts >= starts:
                msg = "Pricing start date should be greater than %s" % starts
                raise be.errors.ErrorWithHint(msg)
            old_pricing_ends = starts - datetime.timedelta(1)
            pricing_resource.set(old_pricing.id, 'ends', old_pricing_ends)
        return pricing_store.add(plan=plan_id, resource=resource_id, starts=starts, amount=amount)

    def destroy(self, plan_id):
        raise NotImplemented

    def list(self, plan_id, for_date):
        """
        returns list of pricings for the plan
        """
        raise NotImplemented

    def list_for_resource(self, resource_id):
        """
        returns list of pricings for specified resource
        """
        raise NotImplemented

class PricingResource:

    def info(self, pricing_id):
        result = pricing_store.get(pricing_id)
        result['starts'] = result['starts'].isoformat()
        result['ends'] = result['ends'].isoformat() if result['ends'] else result['ends']
        return result

    def update(self, plan_id, resource_prices):
        """
        resource_prices: a tuple containing resource_id, prices and date from which the pricing will be activated
        """
        raise NotImplemented

pricing_collection = PricingCollection()
pricing_resource = PricingResource()

import datetime
import be.repository.access as dbaccess
import be.errors

pricing_store = dbaccess.pricing_store

class PricingCollection:

    def new(self, plan_id, resource_prices):
        """
        resource_prices: a tuple containing resource_id, price and date from which the price will be activated
        """
        # check if a record  with same plan_id and starts exists
        # multi insert
        price_ids = []
        for resource_id, amount, from_date in resource_prices:
            pricing = dbaccess.get_resource_pricing(plan=plan_id, resource=resource_id)
            if pricing.starts == from_date: # price change detected
                # find all usages using this pricing
                # warn user about such usages getting affected. Show invoiced and un-invoiced
                # allow user to call same api with force_update_usages=1
                pass
            if pricing:
                # end earlier price
                pricing_store.update_by(crit=dict(plan=plan_id, resource=pricing.resource_id, start=pricing.starts,ends=pricing.ends), amount=amount)
            # create new pricing
            price_id = pricing_store.add(plan=plan_id, resource=resource_id, start=from_date, amount=amount)
            price_ids.append(price_id)

        return price_ids

    def new(self, resource_id, plan_id, starts, amount):
        # starts should be greater than last pricings start which has no 'ends' date yet
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

class PricingResource:

    def info(self, pricing_id):
        return pricing_store.get(pricing_id)

    def update(self, plan_id, resource_prices):
        """
        resource_prices: a tuple containing resource_id, prices and date from which the pricing will be activated
        """
        raise NotImplemented

pricing_collection = PricingCollection()
pricing_resource = PricingResource()

Member states
=============

Active
------
Currently host mark a member 'not active. usually when the member is no longer on some tariff but still associated with the Hub. Active flag is confusing for many hosts and they use it as per their interpretation. Hubspace software excludes inactive member from search by other members (except hosts of member's homehub) and also excludes in other processes such as invoicing search.There is not much point in carrying this concept forward. A member who is not on tariff of a Hub will be excluded in default search. In case Hub still wants such a member in search host may put such a member on guest tariff.

Member Attributes
=================

Home Hub
--------
Hubspace has homehub concept where a member is attached one of hubs and software treats that hub as homehub of that member where in some cases granting special priviledges to hosts of the hub on that member. This is no longer required. One member may be a member of multiple hubs i.e. on tariffs for such hubs. Members sometime switch hub memberships so if earlier hub sets member 'not active' other one soon needs to activate.

Tax calculation
===============
- There could be more than one level of taxes.
- There should be default Tax levels per location
- Resource tax overrides location tax levels

Cost calculation
================
Rules

- If custom cost no processing needed
- Usual cost calculation
    member->tariff->pricing->resource price
    get_price(resource_id, usage_time)
- Taxes
    get_tax_for_resource(resource_id):
- Other rules

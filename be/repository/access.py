import cPickle
import datetime
import psycopg2
import be.repository.stores as stores_mod
import bases.persistence

ctxsep = ':'

PGBinary = bases.persistence.PGBinary

user_store = stores_mod.User()
contact_store = stores_mod.Contact()
member_store = stores_mod.Member()
memberpref_store = stores_mod.MemberPref()
memberprofile_store = stores_mod.MemberProfile()
registered_store = stores_mod.Registered()
session_store = stores_mod.Session()
userpermission_store = stores_mod.UserPermission()
userrole_store = stores_mod.UserRole()
bizplace_store = stores_mod.BizPlace()
bizplaceprofile_store = stores_mod.BizplaceProfile()
request_store = stores_mod.Request()
requestpermission_store = stores_mod.RequestPermission()
membership_store = stores_mod.Membership()
resource_store = stores_mod.Resource()
resourcerelation_store = stores_mod.ResourceRelation()
usage_store = stores_mod.Usage()
invoice_store = stores_mod.Invoice()
pricing_store = stores_mod.Pricing()
activity_store = stores_mod.Activity()
activityaccess_store = stores_mod.ActivityAccess()
invoicepref_store = stores_mod.InvoicePref()
billingpref_store = stores_mod.BillingPref()
oidgen_store = stores_mod.OidGen()

class RStore(object): pass

def make_rstore(store):
    rstore = RStore()
    for attr in ('setup', 'add', 'add_many', 'remove', 'remove_by', 'remove_many', 'get', 'get_many', 'get_by', 'get_one_by', 'get_all', 'update', 'update_many', 'update_by', 'count'):
        method = getattr(store, attr)
        setattr(rstore, attr, method)
    return rstore

class stores: pass

stores_by_type = {}

for name, store in stores_mod.known_stores.items():
    setattr(stores, name, make_rstore(store))
    stores_by_type[store.__class__.__name__] = store

def find_memberships(member_id):
    return membership_store.get_by(crit=dict(member_id=member_id))

def biz_info(biz_id):
    return biz_store.get(biz_id, ['name', 'state', 'short_description', 'currency', 'address', 'city', 'country', 'email'])

bizplace_info_fields = ['id', 'name', 'state', 'short_description', 'currency',
'address', 'city', 'country', 'email', 'phone', 'fax','host_email',
'booking_email', 'website', 'tz']

def bizplace_info(bizplace_id):
    return bizplace_store.get(bizplace_id, bizplace_info_fields)

class Resource(object):
    store = resource_store
    info_fields = ['id', 'name', 'short_description']
    def info(self):
        return self.store.get(self.id, self.info_fields)
    def dependencies(self):
        deps = self.store.get(self.id, ['contains', 'contains_opt', 'requires', 'suggests', 'contained_by', 'required_by', 'suggested_by'])
        dep_ids = list(itertools.chain(*deps.values()))
        return resource_store.get_many(dep_ids, self.info_fields)


def list_activities_by_categories(catesgories, from_date, to_date, limit=20):
    clause = '( category IN %(categories)s) AND created >= %(from_date)s AND created <= %(to_date)s ORDER BY created DESC LIMIT %(limit)s'
    clause_values = dict(categories=tuple(categories), from_date=from_date, to_date=to_date, limit=limit)
    return activity_store.get_by_clause(clause, clause_values, fields=None, hashrows=True)

def list_activities_by_names(names, from_date, to_date, limit=20):
    clause = '(name IN %(names)s) AND created >= %(from_date)s AND created <= %(to_date)s ORDER BY created DESC LIMIT %(limit)s'
    clause_values = dict(names=tuple(names), from_date=from_date, to_date=to_date ,limit=limit)
    return activity_store.get_by_clause(clause, clause_values, fields=None, hashrows=True)

def list_activities_by_roles(roles, limit=15):
    clause = 'role IN %(roles)s GROUP BY created, a_id ORDER BY created DESC LIMIT %(limit)s '
    clause_values = dict(roles=tuple(roles), limit=limit)
    a_ids = [row[0] for row in activityaccess_store.get_by_clause(clause, clause_values, fields=['a_id'], hashrows=False)]
    clause = '(id IN %(a_ids)s) ORDER BY created DESC'
    clause_values = dict(a_ids = tuple(a_ids))
    return activity_store.get_by_clause(clause, clause_values, fields=[], hashrows=True) if len(a_ids)!=0 else []

def find_activities(member_ids=[], roles=[], limit=15):
    clause = ''
    if member_ids:
        clause += "(member_id = %s) "
    if roles:
        clause += ' OR '
        role_clauses = ["(role_ctx = %s AND role_name = %s)" for role in roles]
        clause += ' OR '.join(role_clauses)
        clause += ' ORDER BY a_id DESC limit %s' % limit
    clause_values = [tuple(member_ids)]
    for role in roles:
        clause_values.extend(role)
    a_ids = tuple(row[0] for row in activityaccess_store.get_by_clause(clause, clause_values, fields=['a_id'], hashrows=False))
    if a_ids:
        clause = '(id IN %(a_ids)s) '
    clause += ' ORDER BY created DESC limit %(limit)s'
    clause_values = dict(a_ids = a_ids, limit=limit)
    return activity_store.get_by_clause(clause, clause_values, fields=[], hashrows=True) if a_ids else []

def list_resources_and_tariffs(owner, fields, type=None):
    clause = "owner = %(owner)s"
    clause_values = dict(owner=owner)
    if type:
        clause += " AND type = %(type)s"
        clause_values['type'] = type
    clause += " ORDER BY name"
    return resource_store.get_by_clause(clause, clause_values, fields)

def list_resources(owner, fields, type=None):
    clause = "type != 'tariff' AND owner = %(owner)s ORDER BY name"
    if type:
        clause = "type = %(type)s AND " + clause
    clause_values = dict(owner=owner, type=type)
    return resource_store.get_by_clause(clause, clause_values, fields)

def oid2name(oid):
    if oid is 0: return 'Global'
    store = stores_by_type[OidGenerator.get_otype(oid)]
    return store.get(oid, ['name'], hashrows=False)

def oid2o(oid):
    store = stores_by_type[OidGenerator.get_otype]
    return store.get(int(oid))

def get_passphrase_by_username(username):
    return user_store.get_by(crit={'username': username})[0].password

def add_membership(member_id, plan_id):
    plan = resource_store.get(plan_id)
    bizplace_name = bizplace_store.get(bizplace_id, fields=['name']).name
    data = dict(plan_id=plan_id, member_id=member_id, plan_name=plan.name, bizplace_id=plan.bizplace_id, bizplace_name=bizplace_name)
    membership_store.add(**data)
    return True

def find_bizplace_members(bizplace_ids, fields=['member', 'name']):
    bizplace_ids = tuple(bizplace_ids)
    clause = 'member IN (SELECT member_id FROM membership WHERE bizplace_id IN %s)'
    clause_values = (bizplace_ids,)
    return memberprofile_store.get_by_clause(clause, clause_values, fields)

tariff_info_fields = ['id', 'name', 'owner', 'short_description']

def find_bizplace_plans(bizplace_id, fields):
    return resource_store.get_by(crit={'owner':bizplace_id, 'type':'tariff'}, fields=fields)

def list_bizplaces(ids):
    return bizplace_store.get_many(ids,fields=bizplace_info_fields) if ids else []

def list_all_bizplaces():
    return bizplace_store.get_all(fields=bizplace_info_fields)

def find_tariff_members(plan_ids, at_time=None, fields=['member', 'name']):
    plan_ids = tuple(plan_ids)
    if not at_time: at_time = datetime.datetime.now()
    clause = 'member IN (SELECT member_id FROM membership WHERE tariff_id IN %(plan_ids)s AND starts <= %(at_time)s AND (ends >= %(at_time)s OR ends is NULL))'
    clause_values = dict(plan_ids=plan_ids, at_time=at_time)
    return memberprofile_store.get_by_clause(clause, clause_values, fields) # TODO not all member fields are necessary


def find_usage(start, end, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types, uninvoiced=False):
    clauses = []

    if start: clauses.append('start_time >= %(start_time)s')
    if end: clauses.append('start_time <= %(end_time)s')
    if invoice_id: clauses.append('invoice = %(invoice_id)s')
    if res_owner_ids: clauses.append('(resource_id IN (SELECT id FROM resource WHERE owner IN %(owner_ids)s))')
    if resource_ids: clauses.append('(resource_id IN %(resource_ids)s)')
    if member_ids: clauses.append('(member IN %(member_ids)s)')
    if resource_types: clauses.append('(resource_id IN (SELECT id FROM resource WHERE type IN %(resource_types)s))')
    if uninvoiced: clauses.append('invoice IS null')
    
    clauses_s = ' AND '.join(clauses)
    clause_values = dict(start_time=start, end_time=end, invoice=invoice_id, resource_ids=tuple(resource_ids), owner_ids=tuple(res_owner_ids), member_ids=tuple(member_ids), resource_types=tuple(resource_types))

    fields = ['resource_name', 'start_time', 'end_time', 'quantity', 'cost', 'id']
    return usage_store.get_by_clause(clauses_s, clause_values, fields=fields)

def get_member_plan_id(member_id, bizplace_id, date, default=True):
    clause = 'member_id = %(member_id)s AND bizplace_id = %(bizplace_id)s AND starts <= %(date)s AND (ends >= %(date)s OR ends IS NULL)'
    values = dict(member_id=member_id, date=date, bizplace_id=bizplace_id)
    plan_ids = membership_store.get_by_clause(clause, values, fields=['tariff_id'], hashrows=False)
    if plan_ids:
        return plan_ids[0][0]
    elif default:
        return bizplace_store.get(bizplace_id, fields=['default_tariff'], hashrows=False)

def get_member_membership(member_id, bizplace_id, date):
    clause = 'member_id = %(member_id)s AND bizplace_id = %(bizplace_id)s AND starts <= %(date)s AND (ends >= %(date)s OR ends IS NULL)'
    values = dict(member_id=member_id, date=date, bizplace_id=bizplace_id)
    memberships = membership_store.get_by_clause(clause, values)
    if memberships:
        return memberships[0]

def get_member_tariff_history(member_id, bizplace_ids=[]):
    date = datetime.datetime.now()
    clause = '(member_id = %(member_id)s) AND (ends <= %(date)s)'
    if bizplace_ids:
        clause += ' AND bizplace_id IN %(bizplace_ids)s'
    values = dict(member_id=member_id, date=date, bizplace_ids=bizplace_ids)
    return membership_store.get_by_clause(clause, values)

def get_member_current_memberships(member_id, bizplace_ids=[]):
    date = datetime.datetime.now().date()
    clause = '(member_id = %(member_id)s) AND (starts <= %(date)s) AND (ends IS NULL OR ends >= %(date)s)'
    if bizplace_ids:
        clause += ' AND bizplace_id IN %(bizplace_ids)s'
    values = dict(member_id=member_id, date=date, bizplace_ids=bizplace_ids)
    return membership_store.get_by_clause(clause, values)

def get_member_memberships(member_id, bizplace_ids=[], since=None, not_current=False):
    current_date = datetime.datetime.now()
    if not since:
        since =  current_date - datetime.timedelta(365)
    clause = '(member_id = %(member_id)s) AND (ends >= %(since)s OR ends IS null)'
    if not_current:
        clause += ' AND ((starts > %(current_date)s) OR (ends < %(current_date)s))'
    if bizplace_ids:
        clause += ' AND bizplace_id IN %(bizplace_ids)s'
    values = dict(member_id=member_id, since=since, bizplace_ids=bizplace_ids, current_date=current_date)
    return membership_store.get_by_clause(clause, values)

def list_invoices(issuer ,limit):
    query = "SELECT invoice.id, member.name, invoice.cost, invoice.created as created, invoice.id FROM member, invoice WHERE member.id = invoice.member AND issuer = %(issuer)s ORDER BY created DESC LIMIT %(limit)s"
    values = dict(issuer = issuer, limit = limit) 
    return invoice_store.query_exec(query, values, hashrows=False)

def search_member(query_parts, options, limit, mtype):
    fields = ['id', 'name']
    query = 'SELECT member.id, member.name, member.email, member.name as label FROM member'
    clause = ""
    if [0,'admin'] not in env.context.roles and options['mybizplace']: # TODO: change this post 0.2
        query += ', membership'
        clause = 'membership.member_id = Member.id AND membership.bizplace_id = (SELECT bizplace_id FROM membership where member_id = %(member_id)s) AND ' 
    if len(query_parts) == 1:
        try:
            query_parts[0] = int(query_parts[0])
            clause += 'Member.id = %(query_part)s'
        except:
            query_parts[0] = query_parts[0] + "%"
            clause += '(Member.first_name ILIKE %(query_part)s OR Member.last_name ILIKE %(query_part)s OR Member.name ILIKE %(query_part)s OR Member.email ILIKE %(query_part)s)'
        values = dict(query_part=query_parts[0], limit=limit)
    elif len(query_parts) == 2:
        clause += '((Member.first_name ILIKE %(query_part1)s AND Member.last_name ILIKE %(query_part2)s) OR (Member.first_name ILIKE %(query_part2)s AND Member.last_name ILIKE %(query_part1)s))'
        values = dict(query_part1=query_parts[0], query_part2=query_parts[1]+"%", limit=limit)
    if mtype != "member":
        values['mtype'] = mtype
    query  += ' WHERE '+clause+' LIMIT %(limit)s'
    values['member_id'] =  env.context.user_id
    
    return member_store.query_exec(query, values)

def get_resource_pricing(plan_id, resource_id, usage_time):
    clause = 'plan = %(plan)s AND resource = %(resource)s AND starts <= %(usage_time)s AND (ends >= %(usage_time)s OR ends is NULL)'
    values = dict(plan=plan_id, resource=resource_id, usage_time=usage_time)
    return pricing_store.get_by_clause(clause, values, fields=['id', 'plan', 'starts', 'ends', 'amount'])

def get_default_pricing(resource_id, usage_time):
    bizplace_id = resource_store.get(resource_id).owner
    default_tariff_id = bizplace_store.get(bizplace_id).default_tariff
    return get_resource_pricing(default_tariff_id, resource_id, usage_time)

def get_resource_pricings(resource_id, usage_time):
    # Along with tariff_id we also need tariff_name so we have a join (clause_resource)
    # instead of join if there are 2 independent queries, would it be any faster?
    q = 'SELECT pricing.id, amount, starts, ends, pricing.plan as tariff_id, resource.name as tariff_name from pricing, resource WHERE'
    clause_pricing = 'resource = %(resource)s AND starts <= %(usage_time)s AND (ends >= %(usage_time)s OR ends is NULL)'
    clause_resource = 'pricing.plan = resource.id ORDER BY resource.name ASC'
    q = ' '.join((q, clause_pricing, 'AND', clause_resource))
    values = dict(resource=resource_id, usage_time=usage_time)
    return pricing_store.query_exec(q, values)

def get_tariff_pricings(tariff_id, usage_time):
    clause = 'plan = %(tariff_id)s AND starts <= %(usage_time)s AND (ends >= %(usage_time)s OR ends is NULL)'
    values = dict(tariff_id=tariff_id, usage_time=usage_time)
    pricings = dict(pricing_store.get_by_clause(clause, values, fields=['resource', 'amount'], hashrows=False))
    resource_ids = list(pricings.keys())
    resources = resource_store.get_many(resource_ids, fields=['id', 'name'])
    for res in resources:
        res['price'] = pricings[res.id]
    return resources

def get_price(resource_id, member_id, usage_time):
    # TODO: if resource owner is not bizplace then?
    bizplace_id = resource_store.get(resource_id, fields=['owner'], hashrows=False)
    plan_id = get_member_plan_id(member_id, bizplace_id, usage_time)
    pricing = get_resource_pricing(plan_id, resource_id, usage_time)
    if pricing:
        return pricing[0].amount

def remove_user_roles(user_id, roles, context):
    clause = 'user_id = %(user_id)s AND context = %(context)s AND role IN %(roles)s'
    userrole_store.remove_by_clause(clause, dict(user_id=user_id, roles=tuple(roles), context=context))

def remove_all_roles_for_user(user_id, context):
    clause = 'user_id = %(user_id)s AND context = %(context)s'
    userrole_store.remove_by_clause(clause, dict(user_id=user_id, context=context))

def remove_user_permissions(user_id, permissions, context):
    clause = 'user_id = %(user_id)s AND context = %(context)s AND permission IN %(permissions)s'
    userpermission_store.remove_by_clause(clause, dict(user_id=user_id, permissions=tuple(permissions), context=context))

def search_invoice(query_parts, options, limit):
    fields = ['id', 'member']
    query = 'SELECT invoice.id, invoice.member FROM invoice, member'
    clause = ""
    if [0, 'admin'] not in env.context.roles or options['mybizplace']:
        query += ', membership'
        clause = 'membership.member_id = Member.id AND membership.bizplace_id = (SELECT bizplace_id FROM membership where member_id = %(member_id)s) AND'
    if len(query_parts) == 1:
        try:
            query_parts[0] = int(query_parts[0])
            clause += ' invoice.id = %(query_part)s'
        except:
            query_parts[0] = query_parts[0] + "%"
            clause += ' (member.first_name ILIKE %(query_part)s OR member.last_name ILIKE %(query_part)s)'
        values = dict(query_part=query_parts[0], limit=limit)
    elif len(query_parts) == 2:
        clause += '((member.first_name ILIKE %(query_part1)s AND member.last_name ILIKE %(query_part2)s) OR (member.first_name ILIKE %(query_part2)s AND member.last_name ILIKE %(query_part1)s))'
        values = dict(query_part1=query_parts[0], query_part2=query_parts[1]+"%", limit=limit)
    query  += ' WHERE '+clause+' AND member.id=invoice.member LIMIT %(limit)s'
    values['member_id'] =  env.context.user_id

    return member_store.query_exec(query, values)

def find_requests_for_approval(perms):
    ctx_perms = tuple((str(c) + ctxsep + p) for c, p in perms)
    clause = " permission IN %(ctx_perms)s"
    values = dict(ctx_perms=ctx_perms)
    req_ids = tuple(row[0] for row in requestpermission_store.get_by_clause(clause, values, fields=['request'], hashrows=False))
    return request_store.get_many(req_ids)

class OidGenerator(object):

    @staticmethod
    def next(otype):
        return oidgen_store.add(**dict(type=otype))

    @staticmethod
    def get_otype(oid):
        return oidgen_store.get(oid, fields=['type'])

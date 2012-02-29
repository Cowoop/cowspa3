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
event_store = stores_mod.Event()
invoice_store = stores_mod.Invoice()
pricing_store = stores_mod.Pricing()
activity_store = stores_mod.Activity()
activityaccess_store = stores_mod.ActivityAccess()
invoicepref_store = stores_mod.InvoicePref()
oidgen_store = stores_mod.OidGen()
messagecust_store = stores_mod.MessageCust()
taxexemption_store = stores_mod.TaxExemption()

class RStore(object): pass

def make_rstore(store):
    rstore = RStore()
    for attr in ('setup', 'add', 'add_many', 'remove', 'remove_by', 'remove_many', 'get', 'get_many', 'get_by', 'get_one_by', 'get_one_by_safe', 'get_all', 'update', 'update_many', 'update_by', 'count', 'query_exec'):
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
    return biz_store.get(biz_id, ['name', 'enabled', 'short_description', 'currency', 'address', 'city', 'country', 'email'])

bizplace_info_fields = ['id', 'name', 'enabled', 'short_description', 'currency', 'address', 'city', 'province', 'country', 'email', 'phone', 'fax','host_email', 'booking_email', 'website', 'tz']

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
    roles = []
    for role in roles:
        ctx = role['context']
        for name in role['roles']:
            roles.append((ctx, name))
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

def oids2names(oids, otype=None):
    """
    oids: list/tuple of oids. All oids assumed to be of same type
    returns object id to name map
    """
    names = {}
    oids = tuple(oids)
    if 0 in oids: names[0] = 'Global'
    if 1 in oids: names[1] = env.config.system_username
    if oids:
        store = stores_by_type[otype or OidGenerator.get_otype(oids[0])]
        names.update(store.get_many(oids, fields=['id', 'name'], hashrows=False))
    return names

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

def find_bizplace_members(bizplace_ids, fields=['member', 'name'], hashrows=True):
    bizplace_ids = tuple(bizplace_ids)
    clause = 'member IN (SELECT member_id FROM membership WHERE bizplace_id IN %s)'
    clause_values = (bizplace_ids,)
    return member_store.get_by_clause(clause, clause_values, fields, hashrows)

def find_bizplace_members_with_membership(bizplace_id, fields=['name', 'member_id', 'tariff_name', 'email'], at_time=None, hashrows=True):
    at_time = at_time if at_time else datetime.datetime.now()
    q = 'SELECT '+", ".join(fields)+' from member, membership WHERE member.id = membership.member_id'
    q += ' AND starts <= %(at_time)s AND (ends >= %(at_time)s OR ends is NULL) AND bizplace_id = %(bizplace_id)s'
    values = dict(at_time=at_time, bizplace_id=bizplace_id)
    return member_store.query_exec(q=q, values=values, hashrows=hashrows)

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


def find_usage(start=None, end=None, starts_on_or_before=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[], uninvoiced=False, exclude_credit_usages=False, calc_mode=[], exclude_cancelled_usages=False):

    clauses = []
    if resource_ids: clauses.append('(id IN %(resource_ids)s)')
    if resource_types: clauses.append('(type IN %(resource_types)s)')
    if calc_mode: clauses.append('calc_mode IN %(calc_mode)s')
    clauses_s = ' AND '.join(clauses)
    clause_values = dict(resource_ids=tuple(resource_ids), member_ids=tuple(member_ids), resource_types=tuple(resource_types), calc_mode=tuple(calc_mode))
    if clauses:
        resource_rows = resource_store.get_by_clause(clauses_s, clause_values, fields=['id'], hashrows=False)
        resource_filter = tuple(row[0] for row in resource_rows)
        if not resource_filter: # no resource matched
            return []
    else:
        resource_filter = tuple()

    clauses = []
    if resource_filter: clauses.append('resource_id IN %(resource_filter)s')
    if res_owner_ids: clauses.append('(resource_owner IN %(owner_ids)s)')
    if start: clauses.append('start_time::Date >= %(start_time)s')
    if end: clauses.append('start_time::Date <= %(end_time)s')
    if starts_on_or_before: clauses.append('start_time::Date <= %(starts_on_or_before)s')
    if invoice_id: clauses.append('invoice = %(invoice_id)s')
    if member_ids: clauses.append('(member IN %(member_ids)s)')
    if uninvoiced: clauses.append('invoice IS null')
    if exclude_credit_usages: clauses.append('cancelled_against IS null')
    if exclude_cancelled_usages: clauses.append('id NOT IN (SELECT cancelled_against FROM usage WHERE cancelled_against IS NOT null)')

    clauses_s = ' AND '.join(clauses) + ' ORDER BY start_time'

    fields = ['member', 'resource_name', 'start_time', 'end_time', 'quantity', 'cost', 'id', 'resource_id', 'created_by', 'total']
    clause_values = dict(start_time=start, end_time=end, invoice=invoice_id, member_ids=tuple(member_ids), resource_filter=resource_filter, owner_ids=tuple(res_owner_ids), starts_on_or_before=starts_on_or_before)
    usages = usage_store.get_by_clause(clauses_s, clause_values, fields=fields)
    member_ids = set([usage.member for usage in usages] + [usage.created_by for usage in usages])
    members = oids2names(member_ids)
    for usage in usages:
        usage['member_name'] = members[usage.member]
        usage['member_id'] = usage.member
        usage['created_by_id'] = usage.created_by
        usage['created_by_name'] = members[usage.created_by]
        del usage['member']
    return usages

def get_member_plan_id(member_id, bizplace_id, date, default=True):
    clause = 'member_id = %(member_id)s AND bizplace_id = %(bizplace_id)s AND starts <= %(date)s AND (ends >= %(date)s OR ends IS NULL)'
    values = dict(member_id=member_id, date=date, bizplace_id=bizplace_id)
    plan_ids = membership_store.get_by_clause(clause, values, fields=['tariff_id'], hashrows=False)
    if plan_ids:
        return plan_ids[0][0]
    elif default:
        return bizplace_store.get(bizplace_id, fields=['default_tariff'], hashrows=False)

def get_member_membership(member_id, bizplace_id, date, exclude_ids=[]):
    """
    exclude_ids = list of membership ids which we want to exclude from result
    """
    clause = 'member_id = %(member_id)s AND bizplace_id = %(bizplace_id)s AND starts <= %(date)s AND (ends >= %(date)s OR ends IS null)'
    if exclude_ids:
        clause += " AND id NOT IN %(exclude_ids)s"
        exclude_ids = tuple(exclude_ids)
    values = dict(member_id=member_id, date=date, bizplace_id=bizplace_id, exclude_ids=exclude_ids)
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
    values = dict(member_id=member_id, date=date, bizplace_ids=tuple(bizplace_ids))
    return membership_store.get_by_clause(clause, values)

def get_member_next_memberships(member_id, date, bizplace_ids=[], exclude_ids=[]):
    clause = '(member_id = %(member_id)s) AND (starts > %(date)s)'
    if bizplace_ids: clause += ' AND bizplace_id IN %(bizplace_ids)s'
    if exclude_ids: clause += ' AND id NOT IN %(exclude_ids)s'
    clause += ' ORDER BY starts LIMIT 1'
    values = dict(member_id=member_id, date=date, bizplace_ids=tuple(bizplace_ids), exclude_ids=tuple(exclude_ids))
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
    clause += ' ORDER BY starts DESC'
    values = dict(member_id=member_id, since=since, bizplace_ids=tuple(bizplace_ids), current_date=current_date)
    return membership_store.get_by_clause(clause, values)

def list_invoices(issuer ,limit):
    query = "SELECT invoice.number, member.name, invoice.total, invoice.created as created, invoice.sent, invoice.id FROM member, invoice WHERE member.id = invoice.member AND issuer = %(issuer)s ORDER BY created DESC"
    if limit is not -1:
        query += " LIMIT %(limit)s"
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
        clause += ' AND type = %(mtype)s'
        values['mtype'] = mtype
    query  += ' WHERE '+clause+' LIMIT %(limit)s'
    values['member_id'] =  env.context.user_id

    return member_store.query_exec(query, values)

def get_resource_pricing(plan_id, resource_id, usage_time, exclude_pricings=[]):
    clause = 'plan = %(plan)s AND resource = %(resource)s AND (starts <= %(usage_time)s OR starts IS NULL) AND (ends >= %(usage_time)s OR ends IS NULL)'
    if exclude_pricings: clause += ' AND id NOT IN %(exclude_pricings)s'
    clause += ' ORDER BY ends DESC'
    values = dict(plan=plan_id, resource=resource_id, usage_time=usage_time, exclude_pricings=tuple(exclude_pricings))
    pricing = pricing_store.get_by_clause(clause, values,  fields=['id', 'plan', 'starts', 'ends', 'amount'])
    return pricing[0] if pricing else None

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

def update_invoice_number(invoice_id, issuer, start_number):

    query = "UPDATE invoice SET number=(SELECT number+1 from (SELECT number FROM invoice WHERE issuer = %(issuer)s UNION select %(starting)s) AS temp_table WHERE number+1 NOT IN (SELECT number FROM invoice WHERE issuer = %(issuer)s AND number IS NOT null) ORDER BY number LIMIT 1), sent=%(sent)s WHERE id=%(invoice_id)s"
    values = dict(issuer=issuer, starting=start_number * 10000000, invoice_id=invoice_id, sent=datetime.datetime.now())
    return invoice_store.query_exec(query, values)

def generate_invoice_number(issuer, start_number, limit=1):

    query = "SELECT number+1 from (SELECT number FROM invoice WHERE issuer = %(issuer)s UNION select %(starting)s) AS temp_table WHERE number+1 NOT IN (SELECT number FROM invoice WHERE issuer = %(issuer)s) ORDER BY number LIMIT %(limit)s"
    values = dict(issuer = issuer, limit = limit, starting = start_number * 10000000)
    return invoice_store.query_exec(query, values, hashrows=False)[0][0]

def generate_invoice_start_number():
    bizplace_invoice_start_offset = 200
    # invoice number starts with bizplace id. old system has used around 100 ids so we start with 200 making sure that new invoice_start allocations do not conflict with old ones
    query = "SELECT count(id) FROM oidgen WHERE type=%(type)s";
    values = dict(type='BizPlace')
    return oidgen_store.query_exec(query, values, hashrows=False)[0][0] + bizplace_invoice_start_offset

def get_count_of_memberships(bizplace, starts, ends, by_tariff=False):
    group_by = "tariff_id" if by_tariff else None
    clause = "bizplace_id=%(bizplace)s AND starts<=%(ends)s AND (ends IS null OR ends>=%(starts)s)"
    clause_values = dict(bizplace=bizplace, starts=starts, ends=ends)
    return membership_store.count_by_clause(clause, clause_values, group_by)

def get_billto_from_pref(pref):
    return pref.owner if pref.mode in (0, 1) else pref.billto

def get_billto_members(members):
    """
    members: list of member.ids
    return dict keyed by member.id, billto
        billto is same as member.id if billing is not redirected
    """
    clause = 'owner IN %(members)s'
    clause_values = dict(members=tuple(members))
    return dict((pref.owner, get_billto_from_pref(pref)) for pref in invoicepref_store.get_by_clause(clause, clause_values, fields=['owner', 'mode', 'billto']))

def get_billfrom_members(member, members=[]):
    if member not in members: members.append(member)
    for member_id in (row[0] for row in invoicepref_store.get_by(dict(billto=member, mode=2), fields=['owner'], hashrows=False)):
        get_billfrom_members(member_id, members)
    return members

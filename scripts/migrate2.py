#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# pip install python-magic

# which location to migrate
# migrate location object
# find resources, migrate
# find pricings, migrate
# find members, migrate
# find usages, migrate
# find invoices, migrate
# find team, migrate
# find message_cust, migrate
# 
import atexit
import cPickle
import datetime
import base64
import magic
import psycopg2
import sys
import os
import docutils
import docutils.core
sys.path.insert(0, '.')
import be
import be.bootstrap
be.bootstrap.start('conf_test')
import be.apps
import commonlib.shared.constants as constants

TEST_RUN = False

mime = magic.Magic(mime=True)
app = be.apps.cowspa

def parse_args():
    global TEST_RUN
    if len(sys.argv) < 3:
        sys.exit("usage: %s <location id> <country code>" % sys.argv[0])
    location_id = int(sys.argv[1])
    country_code = sys.argv[2]
    TEST_RUN = '-t' in sys.argv
    return location_id, country_code

location_id, country_code = parse_args()

def jsonrpc(auth_token, apiname, **kw):
    params = {"jsonrpc": "2.0", "method": apiname, "params": kw, "id": 1}
    result = app.dispatch(auth_token, params)
    if 'error' in result:
        print(result)
        print('Failed: ' + apiname)
        print(result['error']['message'])
        sys.exit(1)
    return result

def import_image(filename):
    return 'data:'
    path = '/tmp/' + filename
    cmd = "scp admin-st@space-hub.nile.the-hub.net:/opt/apphomes/hubspace/hubspace/binaries/%s /tmp/" % filename
    ret = os.system(cmd)
    logo = ('data:' + mime.from_file(path) + ';base64,' + base64.b64encode(open(path).read())) if ret == 0 else None
    return logo

auth_token = jsonrpc(None, "login", username="admin", password="x")['result']['auth_token']

spaceconn = psycopg2.connect("dbname=thehub")
spacecur = spaceconn.cursor()

csconn = psycopg2.connect("dbname=shon")
cscur = csconn.cursor()

debug = True
state_path = 'mig.data'

cscur.execute("SET CLIENT_ENCODING to 'UNICODE'")

class odict(dict):
    def __getattr__(self, attr):
        return self[attr]

def select(cur, q, values=None, hashrows=True):
    if debug: print(q)
    cur.execute(q, values)
    rows = cur.fetchall()
    if cur.description and hashrows:
        cols = tuple(r[0] for r in cur.description)
        return [odict(zip(cols, row)) for row in rows]
    else:
        return rows

def insert(cur, q, values):
    if debug: print(q, v)
    try:
        cursor.execute(q, values)
    except psycopg2.ProgrammingError, err:
        try:
            print(cursor.mogrify(q, values))
        except:
            print("damn, can't even mogrify: [%s], [%s]" % (q, values))
        raise err

def select_object(table_name, id):
    q = 'SELECT * FROM ' + table_name + ' WHERE id=%(id)s'
    values = dict(table_name=table_name, id=id)
    return select(spacecur, q, values)[0]

class mdict(dict): pass

if os.path.exists(state_path):
    f = open(state_path)
    migrated = cPickle.load(f)
    f.close()
else:
    migrated = mdict()
    migrated.location = {}
    migrated.resource = {}
    migrated.member = {}
    migrated.pricing = {}
    migrated.usage = {}
    migrated.membership = {}
    migrated.pending = mdict()
    migrated.pending.usage_created_by = {}

class Object(object):
    unchanged = tuple()
    renamed = {}
    def __init__(self, id):
        self.id = id
        self.data = {}
        self.new_data = {}
    def data_import(self):
        self.data = select_object(self.table_name, self.id)
    def pre(self):
        for name in self.unchanged:
            v = self.data[name]
            if v: self.new_data[name] = v
        for name, newname in self.renamed.items():
            v = self.data[name]
            if v is not None: self.new_data[newname] = v
        for k,v in self.new_data.items():
            if isinstance(v, datetime.datetime):
                v = v.isoformat()
                self.new_data[k] = v
    def post(self): pass
    def export(self): pass
    def migrate(self):
        self.data_import()
        self.pre()
        self.export()
        self.post()

class Location(Object):
    table_name = 'location'
    unchanged = ('name', 'city', 'currency')
    renamed = dict(timezone='tz', url='website', telephone='phone', billing_address='address', homepage_description='long_description')
    def export(self):
        self.new_data.update(dict(short_description='', email=self.data.name.lower() + '.hosts@the-hub.net', country=''))
        self.new_data['country'] = country_code
        self.new_data['skip_default_tariff'] = True
        data = jsonrpc(auth_token, 'bizplace.new', **self.new_data)
        new_location_id = data['result']
        migrated.location[self.id] = new_location_id

        logo_filename = "location-logo-%s" % location_id
        logo = import_image(logo_filename)
        logo_data = dict(bizplace_id=new_location_id, logo=logo)
        jsonrpc(auth_token, 'bizplace.update', **logo_data)

        # defaulttariff_id

class InvoicePref(Object):
    table_name = 'location'
    renamed = dict(invoice_bcc='bcc_email', vat_included='tax_included', invoice_duedate='due_date', payment_terms='terms_and_conditions')
    later = dict(defaulttariff_id='default_tariff')
    def export(self):
        self.new_data['owner'] = migrated.location[self.id]
        invlogo_filename = "location-invlogo-%s" % self.id
        invlogo = import_image(invlogo_filename)
        self.new_data['logo'] = invlogo

        self.new_data['tax_included'] = bool(self.data['vat_included'])
        self.new_data['taxes'] = dict(VAT=self.data['vat_default'])
        self.new_data['company_no'] = self.data['company_no']
        self.new_data['taxation_no'] = self.data['vat_no']
        jsonrpc(auth_token, 'invoicepref.update', **self.new_data)

class Resource(Object):
    table_name = 'resource'
    unchanged = ('name', 'type')
    renamed = dict(description="long_description", time_based="calc_mode")

    def export(self):
        if 'long_description' in self.new_data:
            long_description = self.new_data['long_description']
            self.new_data['long_description'] = docutils.core.publish_parts(long_description, writer_name="html")['html_body']
        if self.data['type'] == 'tariff':
            self.new_data['calc_mode'] = 2
        self.new_data['owner'] = migrated.location[location_id]
        self.new_data['short_description'] = ''
        self.new_data['default_price'] = 0 # this will correct once we import all pricings
        result = jsonrpc(auth_token, 'resource.new', **self.new_data)
        new_resource_id = result['result']
        migrated.resource[self.id] = new_resource_id

        image_filename = "resource-resimage-%s" % self.id
        image = import_image(image_filename)
        state = dict(enabled = bool(self.data['active']))
        mod_data = dict(res_id=new_resource_id, picture=image, state=state)
        if self.data['vat']:
            mod_data['taxes'] = dict(VAT=self.data['vat'])
            mod_data['follow_owner_taxes'] = False
        jsonrpc(auth_token, 'resource.update', **mod_data)

class Pricing(Object):
    table_name = 'pricing'
    renamed = dict(periodstarts='starts', periodends='ends', cost='amount')

    def export(self):
        print self.new_data
        self.new_data['resource_id'] = migrated.resource[self.data['resource_id']]
        self.new_data['tariff_id'] = migrated.resource[self.data['tariff_id']]
        if self.new_data['starts'][:4] in ('1970', '9999'):
            self.new_data['starts'] = None

        result = jsonrpc(auth_token, 'pricings.new', **self.new_data)
        migrated.pricing[self.id] = result['result']

class Member(Object):
    # TODO: relationships dict
    table_name = 'tg_user'
    unchanged = ('first_name', 'last_name', 'mobile', 'fax', 'website', 'address')
    renamed = dict(id='number', display_name='name', email_address='email', user_name='username', skype_id='skype', description='long_description', organisation='organization', password='enc_password')

    def export(self):
        if self.new_data.get('long_description'):
            long_description = self.new_data['long_description']
            self.new_data['long_description'] = docutils.core.publish_parts(long_description, writer_name="html")['html_body']
        self.new_data['state'] = dict(enabled = bool(self.data['active']))

        result = jsonrpc(auth_token, 'member.new', **self.new_data)
        new_member_id = result['result']
        migrated.member[self.id] = new_member_id

        mod_data = dict(member_id=new_member_id, created=self.data['created'])
        #signedby = migrated.member[self.data['signedby_id']]
        #hostcontact = migrated.member[self.data['hostcontact_id']]
        result = jsonrpc(auth_token, 'member.update', **mod_data)

        mode = 0
        if not self.data['bill_to_profile']:
            if self.data['billto_id'] in (self.id, None):
                mode = 1
            else:
                mode = 2

        billing_pref = dict(member=new_member_id, mode=mode)

        if mode == 1:
            billing_pref['details'] = dict(
                name=self.data['bill_to_company'],
                address=self.data['billingaddress'],
                phone=self.data['bill_phone'],
                email=self.data['bill_email'],
                fax=self.data['bill_fax'], # new
                company_no=self.data['bill_company_no'],
                taxation_no=self.data['bill_vat_no']
                )
        elif mode == 2:
            billing_pref['billto'] = migrated.member[self.data['billto_id']]

        jsonrpc(auth_token, 'billingpref.update', **billing_pref)

class Usage(Object):
    table_name = 'rusage'
    unchanged = ('resource_name', 'end_time', 'quantity')
    renamed = dict(start='start_time', date_booked='created')

    def export(self):
        q = 'SELECT id from pricing where tariff_id = %(tariff_id)s AND resource_id = %(resource_id)s AND periodstarts <= %(start)s AND periodends >= %(start)s';
        pricing = select(spacecur, q, self.data, False)[0][0]
        resource_id = migrated.resource[self.data['resource_id']]
        self.new_data['pricing'] = migrated.pricing[pricing]
        self.new_data['resource_id'] = resource_id
        self.new_data['resource_owner'] = migrated.location[location_id]
        self.new_data['member'] = migrated.member[self.data['user_id']]
        if self.data['refund_for']:
            self.new_data['cancelled_against'] = migrated.usage[self.data['refund_for']]
        customcost = self.data.get('customcost', None)
        self.new_data['cost'] = customcost
        self.new_data['calculated_cost'] = self.data['cost']
        self.new_data['amount'] = customcost if customcost is not None else self.data['cost']
        result = jsonrpc(auth_token, 'usage.m_new', **self.new_data)
        new_usage_id = result['result']
        migrated.usage[self.id] = new_usage_id
        if self.data['bookedby_id'] not in migrated.member:
            migrated.pending.usage_created_by[self.id] = self.data['bookedby_id']
        else:
            mod_data = dict(usage_id=new_usage_id, created_by = migrated.member[self.data['bookedby_id']])
            jsonrpc(auth_token, 'usage.update', **mod_data)

class Invoice(Object):
    unchanged = ('sent',)
    def export(self):
        pass


def banner(s):
    print("\n" + s + "\n" + ('-'*len(s)))

def migrate_location():
    banner("Migrating locations")
    location = Location(location_id)
    if location_id in migrated.location:
        print("Skipping id:%d" % location_id)
        new_location_id = migrated.location[location_id]
    else:
        location.migrate()
        new_location_id = migrated.location[location_id]

        banner("Migrating invoicepref")
        invoicepref = InvoicePref(location_id)
        invoicepref.migrate()

    banner("Migrating resources")
    # Create guest tariff
    # Create other tariffs
    # Create rest of the resources
    # Create pricings

    q = 'SELECT defaulttariff_id FROM location WHERE id = %(location_id)s'
    values = dict(location_id=location_id)
    defaulttariff_id = select(spacecur, q, values, False)[0][0]

    # Migrate default tariff
    if not defaulttariff_id in migrated.resource:
        resource = Resource(defaulttariff_id)
        resource.migrate()
    new_defaulttariff_id = migrated.resource[defaulttariff_id]

    values = dict(bizplace_id=new_location_id, default_tariff=new_defaulttariff_id)
    jsonrpc(auth_token, 'bizplace.update', **values)

    q = 'SELECT id FROM resource WHERE place_id=%(location_id)s AND id != %(defaulttariff_id)s'
    values = dict(location_id=location_id, defaulttariff_id=defaulttariff_id)
    all_resource_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    q = "SELECT id FROM resource WHERE place_id=%(location_id)s AND type = 'tariff' AND id != %(defaulttariff_id)s"
    tariff_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    resource_ids = tuple(id for id in all_resource_ids if id not in tariff_ids)

    for id in tariff_ids+resource_ids:
        if id in migrated.resource:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        resource = Resource(id)
        resource.migrate()

    q = 'SELECT id FROM pricing WHERE resource_id IN %(all_resource_ids)s'
    values = dict(all_resource_ids=all_resource_ids)
    pricings = tuple(row[0] for row in select(spacecur, q, values, False))

    for id in pricings:
        if id in migrated.pricing:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        pricing = Pricing(id)
        pricing.migrate()


    banner("Migrating members")
    q = 'SELECT id FROM tg_user WHERE id in (SELECT user_id FROM rusage WHERE resource_id IN %(resource_ids)s)'
    values = dict(resource_ids=resource_ids)
    member_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    q = 'SELECT billto_id FROM tg_user WHERE id in %(member_ids)s AND billto_id IS NOT NULL'
    values = dict(member_ids=member_ids)
    billto_member_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    final_member_ids = list(billto_member_ids)
    for id in member_ids:
        if id not in final_member_ids:
            final_member_ids.append(id)
    for id in final_member_ids:
        if id in migrated.member:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        member = Member(id)
        member.migrate()

    banner("Migrating usages")
    q = 'SELECT id FROM rusage WHERE resource_id IN %(resource_ids)s ORDER BY id'
    values = dict(resource_ids=resource_ids)
    usage_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    for id in usage_ids:
        if id in migrated.usage:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        usage = Usage(id)
        usage.migrate()

    banner("Migrating memberships")
    member_ids = tuple(migrated.member.keys())
    q = "SELECT id, start, end_time, resource_id FROM rusage WHERE resource_id IN (SELECT id FROM resource WHERE place_id = %(location_id)s AND type='tariff') AND user_id = %(member_id)s AND cancelled = 0 AND refund = 0 ORDER BY start"
    for id in member_ids:
        memberships = []
        values = dict(member_id=id, location_id=location_id)
        tariff_usages_ = select(spacecur, q, values)
        if not tariff_usages_:
            continue
        # Found some tariff usages have same start,end. This is not acceptable in Ops
        # So filtering here
        tariff_usages = [tariff_usages_[0]]
        for usage in tariff_usages_[1:]:
            if usage.start == tariff_usages[-1].start:
                tariff_usages[-1] = usage
            else:
                tariff_usages.append(usage)

        usage = tariff_usages[0]
        memberships.append([usage.resource_id, usage.start, usage.end_time])
        for usage in tariff_usages[1:]:
            last = memberships[-1]
            if usage.resource_id == last[0] and usage.start.date() == last[-1].date():
                last[-1] = usage.end_time
            else:
                memberships.append([usage.resource_id, usage.start, usage.end_time])

        for membership in memberships:
            data = dict(tariff_id=migrated.resource[membership[0]], member_id=migrated.member[id], starts=membership[1].isoformat(), \
                ends=(membership[2]-datetime.timedelta(1)).isoformat())
            membership_hash = hash(frozenset(data.items()))
            if not membership_hash in migrated.membership:
                result = jsonrpc(auth_token, 'memberships.new', **data)
                #migrated.membership[membership_hash] = result['result']



def before_exit():
    f = open(state_path, 'w')
    cPickle.dump(migrated, f)
    f.close()

atexit.register(before_exit)
migrate_location()

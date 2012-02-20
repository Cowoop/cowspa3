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
import calendar
import base64
import urllib
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

binaries_dir = 'binaries'
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
    if TEST_RUN:
        return 'data:'
    path = binaries_dir + '/' + filename
    cmd = "scp admin-st@space-hub.nile.the-hub.net:/opt/apphomes/hubspace/hubspace/binaries/%s binaries/" % filename
    ret = os.system(cmd)
    logo = ('data:' + mime.from_file(path) + ';base64,' + base64.b64encode(open(path).read())) if ret == 0 else None
    return logo

def wget(src, dst):
    print("fetching " + src)
    cmd = "wget %(src)s -O %(dst)s" % locals()
    return os.system(cmd)

def download_invoices(old_id, new_id):
    invoice_dir = 'be/repository/invoices'
    paths = [("http://members.the-hub.net/show_invoice/%s", 'html'), ("http://members.the-hub.net/pdf_invoice/%s", 'pdf')]
    for path, format in paths:
        src = path % old_id
        dst = "%s/%s.%s" % (invoice_dir, new_id, format)
        if not os.path.exists(dst):
            ret = wget(src, dst)

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

def get_month_end(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime.datetime(date.year, date.month, last_day)

def select(cur, q, values=None, hashrows=True):
    if debug: print(q, values)
    cur.execute(q, values)
    rows = cur.fetchall()
    if cur.description and hashrows:
        cols = tuple(r[0] for r in cur.description)
        return [odict(zip(cols, row)) for row in rows]
    else:
        return rows

def qexec(cur, q, values={}):
    if debug: print(q, values)
    try:
        cur.execute(q, values)
    except psycopg2.ProgrammingError, err:
        try:
            print(cur.mogrify(q, values))
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
    migrated.invoice = {}
    migrated.pending = mdict()
    migrated.pending.usage_created_by = {}
    migrated.pending.usage_invoices = {}
    migrated.messagecust = {}

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
        self.new_data.update(dict(short_description='', country=''))
        self.new_data['name'] = 'The Hub ' + self.new_data['name']
        self.new_data['email'] = self.data.name.lower() + '.hosts@the-hub.net'
        self.new_data['host_email'] = self.data.name.lower() + '.hosts@the-hub.net'
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

class MessageCust(Object):
    table_name = 'message_customization'
    #unchanged = ('lang',)
    renamed = dict(message='name', text='content')
    def export(self):
        if not self.data['message'].startswith('invoice_freetext'):
            self.new_data['owner_id'] = migrated.location[location_id]
            jsonrpc(auth_token, 'messagecust.new', **self.new_data)
            migrated.messagecust['id'] = None
        else:
            q = 'UPDATE invoice_pref SET %s = %%(content)s WHERE owner = %%(owner)s'
            name = 'freetext1' if self.data['message'].endswith('1') else 'freetext2'
            q = q % name
            values = dict(content=self.data['text'], owner=migrated.location[location_id])
            qexec(cscur, q, values)
            migrated.messagecust['id'] = None

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
        new_resource_id = migrated.resource[self.data['resource_id']]
        self.new_data['resource_id'] = new_resource_id
        self.new_data['tariff_id'] = migrated.resource[self.data['tariff_id']]
        for attr in ('starts', 'ends'):
            if self.new_data[attr][:4] in ('1970', '9999'):
                self.new_data[attr] = None

        q = 'SELECT type FROM resource WHERE id=%(resource_id)s'
        values = dict(resource_id=new_resource_id)
        result = select(cscur, q, values, False)
        type = result[0][0]
        if type == 'tariff':
            q = 'SELECT default_tariff FROM bizplace WHERE id = %(bizplace_id)s'
            values = dict(bizplace_id=migrated.location[location_id])
            result = select(cscur, q, values, False)
            self.new_data['tariff_id'] = result[0][0]

        result = jsonrpc(auth_token, 'pricings.new', **self.new_data)
        migrated.pricing[self.id] = result['result']

class Member(Object):
    # TODO: relationships dict
    table_name = 'tg_user'
    unchanged = ('first_name', 'last_name', 'mobile', 'fax', 'website', 'address')
    renamed = dict(id='number', display_name='name', email_address='email', user_name='username', skype_id='skype', description='long_description', organisation='organization', password='enc_password')

    def export(self):
        billto_id = self.data['billto_id']
        if billto_id not in (self.id, None) and billto_id not in migrated.member:
            Member(billto_id).migrate()
        if self.new_data.get('long_description'):
            long_description = self.new_data['long_description']
            self.new_data['long_description'] = docutils.core.publish_parts(long_description, writer_name="html")['html_body']
        self.new_data['state'] = dict(enabled = bool(self.data['active']))
        self.new_data['first_name'] = self.new_data.get('first_name', '')

        q = 'SELECT * from user_meta_data where user_id = %(user_id)s'
        values = dict(user_id = self.id)
        result = select(spacecur, q, values)
        if result:
            meta = result[0]
            if 'introduced_by' in meta:
                self.new_data['introduced_by'] = meta.introduced_by
            if 'postcode' in meta:
                self.new_data['pincode'] = meta.postcode
            if 'biz_type' in meta:
                self.new_data['biz_type'] = meta.biz_type

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

        q = "SELECT group_name from user_group, tg_group where user_id=%(member_id)s and group_id in (SELECT id from tg_group WHERE place_id = %(location_id)s and (group_name like '%%_director' or group_name like '_%%host')) and tg_group.id = user_group.group_id"
        values = dict(location_id=location_id, member_id=self.id)
        roles = [row[0].split('_')[1] for row in select(spacecur, q, values, False)]
        if roles:
            role_data = dict(user_id=new_member_id, roles=roles, context=migrated.location[location_id])
            result = jsonrpc(auth_token, 'roles.add', **role_data)

class Usage(Object):
    table_name = 'rusage'
    unchanged = ('resource_name', 'end_time', 'quantity', 'notes')
    renamed = dict(start='start_time', date_booked='created', meeting_name='name', meeting_description='description')

    def export(self):
        resource_id = migrated.resource[self.data['resource_id']]
        self.new_data['resource_id'] = resource_id
        self.new_data['resource_owner'] = migrated.location[location_id]
        self.new_data['member'] = migrated.member[self.data['user_id']]
        if self.data['refund_for']:
            if migrated.usage.get(self.data['refund_for']): # there are some refunds which points to non-existent usage
                self.new_data['cancelled_against'] = migrated.usage[self.data['refund_for']]
        customcost = self.data.get('customcost', self.data['cost'])
        self.new_data['cost'] = customcost
        self.new_data['calculated_cost'] = self.data['cost']
        result = jsonrpc(auth_token, 'usage.m_new', **self.new_data)
        new_usage_id = result['result']
        migrated.usage[self.id] = new_usage_id
        if self.data['bookedby_id'] not in migrated.member:
            migrated.pending.usage_created_by[self.id] = self.data['bookedby_id']
        else:
            mod_data = dict(usage_id=new_usage_id, created_by = migrated.member[self.data['bookedby_id']])
            jsonrpc(auth_token, 'usage.update', **mod_data)

class Invoice(Object):
    table_name = 'invoice'
    # TODO cost/amount?
    unchanged = ('number', 'created', 'sent')
    renamed = dict(start='start_date', end_time='end_date', amount='total')
    def export(self):
        if 'start' not in self.new_data:
            self.new_data['start_date'] = self.new_data['end_date']
        self.new_data['member'] = migrated.member[self.data['user_id']]
        self.new_data['issuer'] = migrated.location[self.data['location_id']]
        ponumbers_s = self.data['ponumbers']
        ponumbers = cPickle.loads(str(ponumbers_s)) if ponumbers_s else []
        self.new_data['po_number'] = ponumbers[0:1] or None
        q = 'SELECT id FROM rusage WHERE invoice_id = %(invoice_id)s'
        values = dict(invoice_id=self.id)
        anomolies = (117922, 117925) # resource owned by one location, invoiced by another
        self.new_data['usages'] = [migrated.usage[row[0]] for row in select(spacecur, q, values, False) if row[0] in migrated.usage]
        result = jsonrpc(auth_token, 'invoice.m_new', **self.new_data)
        new_invoice_id = result['result']
        migrated.invoice[self.id] = new_invoice_id
        migrated.pending.usage_invoices[self.id] = [row[0] for row in select(spacecur, q, values, False) if row[0] not in migrated.usage]

    def post(self):
        print("Invoice %s migrattion | post" % self.id)
        new_invoice_id = migrated.invoice[self.id]
        data = dict(invoice_id=new_invoice_id, sent=self.data['sent'], created=self.data['created'])
        jsonrpc(auth_token, 'invoice.update', **data)
        usages = self.new_data['usages']
        if usages:
            q = 'UPDATE usage SET invoice = %(invoice_id)s WHERE id IN %(usages)s'
            values = dict(usages=tuple(usages), invoice_id=new_invoice_id)
            qexec(cscur, q, values)

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

    banner("Migrating members")
    q = 'SELECT id FROM tg_user'
    member_ids = tuple(row[0] for row in select(spacecur, q, {}, False))
    for id in member_ids:
        if id in migrated.member:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        member = Member(id)
        member.migrate()

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


    banner("Migrating usages")
    q = 'SELECT id FROM rusage WHERE resource_id IN (SELECT id FROM resource WHERE place_id = %(location_id)s) ORDER BY id'
    values = dict(location_id=location_id)
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
    q = "SELECT id, start, resource_id FROM rusage WHERE resource_id IN (SELECT id FROM resource WHERE place_id = %(location_id)s AND type='tariff') AND user_id = %(member_id)s AND cancelled = 0 AND refund = 0 ORDER BY start"
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
        memberships.append([usage.resource_id, usage.start, get_month_end(usage.start)])
        for usage in tariff_usages[1:]:
            last = memberships[-1]
            if last[1].date() == usage.start.date():
                continue
            if usage.resource_id == last[0] and usage.start.date() == last[-1].date():
                last[-1] = usage.end_time
            else:
                memberships.append([usage.resource_id, usage.start, get_month_end(usage.start)])

        banner('Migrating memberships of %d' % id)
        print(memberships)
        for membership in memberships:
            data = dict(tariff_id=migrated.resource[membership[0]], member_id=migrated.member[id], starts=membership[1].isoformat(), \
                ends=(membership[2]-datetime.timedelta(1)).isoformat(), skip_usages=True)
            membership_hash = hash(frozenset(data.items()))
            if not membership_hash in migrated.membership:
                result = jsonrpc(auth_token, 'memberships.new', **data)
                migrated.membership[membership_hash] = result['result']

    banner("Migrating Invoices")
    q = 'SELECT id FROM invoice WHERE location_id = %(location_id)s'
    values = dict(location_id=location_id)
    invoice_ids = (row[0] for row in select(spacecur, q, values, False))
    for id in invoice_ids:
        if id in migrated.invoice:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        invoice = Invoice(id)
        invoice.migrate()

    banner("Migrating message_customizations")
    q = 'SELECT id FROM message_customization WHERE location_id = %(location_id)s'
    values = dict(location_id=location_id)
    msg_ids = (row[0] for row in select(spacecur, q, values, False))
    for id in msg_ids:
        if id in migrated.messagecust:
            print("Skipping id:%d" % id)
            continue
        print("migrating id:%d" % id)
        messagecust = MessageCust(id)
        messagecust.migrate()

    banner("Migrating EU Tax Exemptions")
    q = 'SELECT * FROM eu_tax_exemption WHERE location_id = %(location_id)s'
    values = dict(location_id=location_id)
    exemptions = (exemption for exemption in select(spacecur, q, values))
    q = 'INSERT INTO tax_exemption (issuer, member) VALUES (%(issuer)s, %(member)s)'
    for exemption in exemptions:
        print("migrating %s" % exemption.user_id)
        values = dict(member=migrated.member[exemption.user_id], issuer=new_location_id)
        qexec(cscur, q, values)
    q = 'COMMIT'
    qexec(cscur, q)

    banner("Downloding Invoices")
    for old_id, new_id in migrated.invoice.items():
        print('downloding: %s' % old_id)
        if not TEST_RUN: download_invoices(old_id, new_id)

def before_exit():
    f = open(state_path, 'w')
    cPickle.dump(migrated, f)
    f.close()

if not os.path.exists(binaries_dir):
    os.mkdir(binaries_dir)
atexit.register(before_exit)
migrate_location()

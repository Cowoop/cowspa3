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
import argparse
import collections
import itertools
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

jsonrpc_cred = dict(username='admin', password='x')
space_db_string =  'dbname=thehub'
cs_db_string = 'dbname=shon'

binaries_dir = 'binaries'
mime = magic.Magic(mime=True)
app = be.apps.cowspa

def parse_args():
    parser = argparse.ArgumentParser(description='Run cowspa server.')
    global TEST_RUN
    parser.add_argument('location_id', action="store", type=int)
    parser.add_argument('-t', action="store_true", dest='test', default=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', action="store_true", dest='all', default=False)
    group.add_argument('-o', dest='objects', nargs='+', default=False)
    return parser.parse_args()

args = parse_args()
print args
TEST_RUN = args.test
location_id, country_code = args.location_id, '004'
objects_to_import = args.all and ['member', 'resource', 'pricing', 'membership', 'team', 'usage', 'mcust', 'role', 'invoice'] or args.objects

def jsonrpc(auth_token, apiname, **kw):
    params = {"jsonrpc": "2.0", "method": apiname, "params": kw, "id": 1}
    result = app.dispatch(auth_token, params)
    if 'error' in result:
        print(apiname +' <- ' + str(kw))
        print(result)
        print('Failed: ' + apiname)
        print(result['error']['message'])
        raise('jsonrpc failed')
    return result

auth_token = jsonrpc(None, "login", **jsonrpc_cred)['result']['auth_token']

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

spaceconn = psycopg2.connect(space_db_string)
spacecur = spaceconn.cursor()

csconn = psycopg2.connect(cs_db_string)
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
        cur.execute('COMMIT')
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
    anomolies = ()
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
        if self.id in self.anomolies:
            print('Skipping: %s [anomolies])' % self.id)
            return
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
        if self.id == 36: self.new_data['city'] = 'Prague' # Hack for Prague
        if self.id == 38: self.new_data['city'] = 'Oaxaca' # Hack for Prague
        if self.id == 39: self.new_data['city'] = 'Rotterdam' # Hack for Prague
        data = jsonrpc(auth_token, 'bizplace.new', **self.new_data)
        new_location_id = data['result']
        migrated.location[self.id] = new_location_id

        logo_filename = "location-logo-%s" % location_id
        logo = import_image(logo_filename)
        logo_data = dict(bizplace_id=new_location_id, logo=logo)
        jsonrpc(auth_token, 'bizplace.update', **logo_data)


class InvoicePref(Object):
    table_name = 'location'
    unchanged = dict(payment_terms='payment_terms')
    renamed = dict(invoice_bcc='bcc_email', vat_included='tax_included', invoice_duedate='due_date')
    later = dict(defaulttariff_id='default_tariff')
    def export(self):
        self.new_data['owner'] = migrated.location[self.id]
        self.new_data['start_number'] = self.id
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
            new_names = dict(invoice_freetext_1='freetext1', invoice_freetext_2='freetext2', invoice_mail='invoice')
            name = new_names.get(self.data['message'], self.data['message'])
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
        mod_data = dict(res_id=new_resource_id, picture=image, enabled = bool(self.data['active']))
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

        try:
            result = jsonrpc(auth_token, 'pricings.new', **self.new_data)
            migrated.pricing[self.id] = result['result']
        except Exception as err:
            if 'Pricing start date should be greater than' in err.message:
                print("Pricing conflict: Skipping %s as it conflicts with previous pricing")
            migrated.pricing[self.id] = None

class Member(Object):
    # TODO: relationships dict
    table_name = 'tg_user'
    unchanged = ('first_name', 'last_name', 'mobile', 'fax', 'website', 'address')
    renamed = dict(id='number', display_name='name', email_address='email', user_name='username', skype_id='skype', description='long_description', organisation='organization', password='enc_password')
    anomolies = (5701,)

    def export(self):
        billto_id = self.data['billto_id']
        if billto_id not in (self.id, None) and billto_id not in migrated.member:
            Member(billto_id).migrate()
        if self.new_data.get('long_description'):
            long_description = self.new_data['long_description']
            self.new_data['long_description'] = docutils.core.publish_parts(long_description, writer_name="html")['html_body']
        self.new_data['enabled'] = bool(self.data['active'])
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
    renamed = dict(start='start_time', date_booked='created', meeting_name='name', meeting_description='description', number_of_people='no_of_people')

    def export(self):
        repetition_id = self.data['repetition_id']
        if repetition_id not in (self.id, None) and repetition_id not in migrated.usage:
            q = 'SELECT id FROM rusage WHERE id = %(repetition_id)s'
            values = dict(repetition_id=repetition_id)
            if select(spacecur, q, values, False):
                Usage(repetition_id).migrate()
                self.new_data['repetition_id'] = migrated.usage[repetition_id]
        resource_id = migrated.resource[self.data['resource_id']]
        self.new_data['resource_id'] = resource_id
        self.new_data['resource_owner'] = migrated.location[location_id]
        self.new_data['member'] = migrated.member[self.data['user_id']]
        self.new_data['public'] = bool(self.data['public_field'])
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
        usage_ids = [row[0] for row in select(spacecur, q, values, False)]
        self.new_data['usages'] = [migrated.usage[id] for id in usage_ids if id in migrated.usage]
        result = jsonrpc(auth_token, 'invoice.m_new', **self.new_data)
        new_invoice_id = result['result']
        migrated.invoice[self.id] = new_invoice_id
        migrated.pending.usage_invoices[self.id] = [id for id in usage_ids if id not in migrated.usage]

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

    banner("Migrating members")
    q = 'SELECT id FROM tg_user'
    member_ids = tuple(row[0] for row in select(spacecur, q, {}, False))
    if 'member' in objects_to_import:
        for id in member_ids:
            if id in migrated.member:
                print("Skipping id:%d" % id)
                continue
            print("migrating id:%d" % id)
            member = Member(id)
            member.migrate()

    banner("Migrating resources")
    # Create guest tariff
    # Create other tariffs
    # Create rest of the resources
    # Create pricings

    q = 'SELECT defaulttariff_id FROM location WHERE id = %(location_id)s'
    values = dict(location_id=location_id)
    defaulttariff_id = select(spacecur, q, values, False)[0][0]

    # Migrate default tariff
    if 'resource' in objects_to_import:
        if not defaulttariff_id in migrated.resource:
            resource = Resource(defaulttariff_id)
            resource.migrate()
        new_defaulttariff_id = migrated.resource[defaulttariff_id]

        values = dict(bizplace_id=new_location_id, default_tariff=new_defaulttariff_id)
        jsonrpc(auth_token, 'bizplace.update', **values)


    q = 'SELECT id FROM resource WHERE place_id=%(location_id)s'
    values = dict(location_id=location_id, defaulttariff_id=defaulttariff_id)
    all_resource_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    q = "SELECT id FROM resource WHERE place_id=%(location_id)s AND type = 'tariff'"
    tariff_ids = tuple(row[0] for row in select(spacecur, q, values, False))
    resource_ids = tuple(id for id in all_resource_ids if id not in tariff_ids)

    if 'resource' in objects_to_import:
        for id in all_resource_ids:
            if id in migrated.resource:
                print("Skipping id:%d" % id)
                continue
            print("migrating id:%d" % id)
            resource = Resource(id)
            resource.migrate()

    if 'resource' in objects_to_import:
        relations_dict = collections.defaultdict(list)
        q = 'SELECT * FROM resource_dependencies WHERE dependend_id IN (SELECT id FROM resource WHERE place_id = %(location_id)s)'
        values = dict(location_id=location_id)
        dependencies = select(spacecur, q, values)
        for dependency in dependencies:
            relations_dict[dependency.dependend_id].append((True, dependency.required_id))
        q = 'SELECT * FROM resource_suggestions WHERE suggesting_id IN (SELECT id FROM resource WHERE place_id = %(location_id)s)'
        values = dict(location_id=location_id)
        suggestions = select(spacecur, q, values)
        for suggestion in suggestions:
            relations_dict[suggestion.suggesting_id].append((False, suggestion.suggested_id))

        for resource_id, relations in relations_dict.items():
            resource_id = migrated.resource[resource_id]
            relations = [(relation[0], migrated.resource[relation[1]]) for relation in relations]
            params = dict(res_id=resource_id, relations=relations)
            jsonrpc(auth_token, 'resource.set_relations', **params)

    q = 'SELECT id FROM pricing WHERE resource_id IN %(all_resource_ids)s'
    values = dict(all_resource_ids=all_resource_ids)
    pricings = tuple(row[0] for row in select(spacecur, q, values, False))

    if 'pricing' in objects_to_import:
        for id in pricings:
            if id in migrated.pricing:
                print("Skipping id:%d" % id)
                continue
            print("migrating id:%d" % id)
            pricing = Pricing(id)
            pricing.migrate()


    banner("Migrating usages")
    if 'usage' in objects_to_import:

        q = 'SELECT id FROM rusage WHERE resource_id IN %(all_resource_ids)s ORDER BY id'
        values = dict(location_id=location_id, all_resource_ids=all_resource_ids)
        usage_ids = tuple(row[0] for row in select(spacecur, q, values, False))
        for id in usage_ids:
            if id in migrated.usage:
                print("Skipping id:%d" % id)
                continue
            print("migrating id:%d" % id)
            usage = Usage(id)
            usage.migrate()

        q = 'SELECT usagesuggestedby_id, id FROM rusage WHERE usagesuggestedby_id IS NOT null AND resource_id IN %(resource_ids)s ORDER BY usagesuggestedby_id limit 3'
        values = dict(resource_ids=resource_ids)
        suggestions = select(spacecur, q, values, False)
        suggestions_grouped = itertools.groupby(suggestions, lambda s: s[0])
        for usage_id, grp in suggestions_grouped:
            suggested = [item[1] for item in grp]
            values = dict(usage_id=migrated.usage[usage_id], usages=[migrated.usage[id] for id in suggested])
            q = 'UPDATE usage SET usages_suggested = %(usages)s WHERE id = %(usage_id)s'
            qexec(cscur, q, values)


    banner("Migrating memberships")
    if 'membership' in objects_to_import:
        q = "SELECT id FROM resource WHERE place_id = %(location_id)s AND type='tariff'"
        values = dict(location_id=location_id)
        resource_ids = tuple(row[0] for row in select(spacecur, q, values, False))
        q = "SELECT DISTINCT user_id FROM rusage WHERE resource_id in %(resource_ids)s"
        values = dict(resource_ids=resource_ids)
        member_ids = tuple(row[0] for row in select(spacecur, q, values, False))
        q = "SELECT id FROM tg_user WHERE homeplace_id = %(location_id)s AND active = 1"
        values = dict(location_id=location_id)
        home_place_member_ids = tuple(row[0] for row in select(spacecur, q, values, False))
        member_ids_w_memberships = set(member_ids + home_place_member_ids)
        for id in member_ids_w_memberships:
            banner('Migrating memberships of %d' % id)
            q = "SELECT id, start, end_time, resource_id FROM rusage WHERE resource_id IN %(resource_ids)s AND user_id = %(member_id)s AND cancelled = 0 AND refund = 0 ORDER BY start"
            memberships = []
            old_member_id = id
            values = dict(member_id=id, location_id=location_id, resource_ids=resource_ids)
            tariff_usages_ = select(spacecur, q, values)
            if tariff_usages_:
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

                for membership in memberships:
                    data = dict(tariff_id=migrated.resource[membership[0]], member_id=migrated.member[id], \
                        starts=membership[1].isoformat(), \
                        ends=(membership[2]-datetime.timedelta(1)).isoformat(), skip_usages=True)
                    membership_hash = hash(frozenset(data.items()))
                    if not membership_hash in migrated.membership:
                        result = jsonrpc(auth_token, 'memberships.new', **data)
                        migrated.membership[membership_hash] = result['result']


                if not memberships or \
                        (tariff_usages[-1].end_time != None or tariff_usages[-1].end_time <= datetime.datetime.now()):
                    starts = datetime.datetime.now()
                    if tariff_usages[-1].end_time != None:
                        starts = tariff_usages[-1].end_time.date() + datetime.timedelta(1)

                    data = dict(tariff_id=migrated.resource[defaulttariff_id], member_id=migrated.member[old_member_id],
                        starts=starts.isoformat(), ends=None, skip_usages=True)
                    jsonrpc(auth_token, 'memberships.new', **data)

            else: # not tariff_usages
                data = dict(tariff_id=migrated.resource[defaulttariff_id], member_id=migrated.member[old_member_id],
                    starts=datetime.datetime.now().isoformat(), ends=None, skip_usages=True)
                jsonrpc(auth_token, 'memberships.new', **data)



    banner("Migrating roles")
    if 'role' in objects_to_import:
        for id in member_ids:
            if id not in migrated.member:
                continue
            banner('Migrating team membership of %d' % id)
            q = "SELECT group_name from user_group, tg_group where user_id=%(member_id)s and group_id in (SELECT id from tg_group WHERE place_id = %(location_id)s and (group_name like '%%_director' or group_name like '_%%host')) and tg_group.id = user_group.group_id"
            values = dict(location_id=location_id, member_id=id)
            roles = [row[0].split('_')[1] for row in select(spacecur, q, values, False)]
            if roles:
                role_data = dict(user_id=migrated.member[id], roles=roles, context=migrated.location[location_id])
                result = jsonrpc(auth_token, 'roles.add', **role_data)


    banner("Migrating Invoices")
    if 'invoice' in objects_to_import:
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
    if 'mcust' in objects_to_import:
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

    banner("Downloding Invoices")
    if 'invoice' in objects_to_import:
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

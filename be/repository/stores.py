import bases.persistence

PGStore = bases.persistence.PGStore

known_stores = {}

def cursor_getter(*ingored):
    return env.context.pgcursor

class PGStore(PGStore):
    cursor_getter = cursor_getter
    def __init__(self):
        store_name = self.__class__.__name__.lower() + '_store'
        known_stores[store_name] = self

# using VARCHAR for username ensures indexing does not fail due to larger text size
class User(PGStore):
    table_name = "account"
    create_sql = """
    id INTEGER NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    enabled BOOLEAN DEFAULT True
    """

class Contact(PGStore):
    table_name = "contact"
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    address TEXT DEFAULT '',
    city TEXT DEFAULT '',
    province TEXT DEFAULT '',
    country TEXT DEFAULT '',
    pincode TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    mobile TEXT DEFAULT '',
    work TEXT DEFAULT '',
    home TEXT DEFAULT '',
    fax TEXT DEFAULT '',
    email TEXT NOT NULL,
    skype TEXT DEFAULT ''
    """

class MemberPref(PGStore):
    table_name = "member_pref"
    create_sql = """
    member INTEGER NOT NULL,
    theme TEXT DEFAULT 'default',
    language TEXT DEFAULT 'en'
    """

class MemberServices(PGStore):
    table_name = "member_service"
    create_sql = """
    member TEXT NOT NULL,
    webpage boolean default false NOT NULL
    """

#class MemberProfileSecurity(PGStore):
#    #membership_id = IntegerField(required=True)
#    property_name = Attribute(required=True)
#    #level = ListField(required=True) # 0 off 1 on: [anonymous access][all locations][same location][private]

class MemberProfile(PGStore):
    table_name = "member_profile"
    create_sql = """
    member INTEGER NOT NULL,
    first_name TEXT,
    last_name TEXT,
    name TEXT NOT NULL,
    introduced_by TEXT,
    short_description TEXT,
    long_description TEXT,
    biz_type TEXT,
    organization TEXT,
    interests TEXT[],
    expertise TEXT[],
    website TEXT,
    blog TEXT,
    twitter TEXT[2],
    facebook TEXT[2],
    linkedin TEXT[2],
    use_gravtar BOOLEAN default false
    """

# Container objects
class Member(PGStore):
    table_name = "member"
    create_sql = """
    id INTEGER NOT NULL,
    number SERIAL NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    enabled BOOLEAN DEFAULT True,
    hidden BOOLEAN DEFAULT False,
    type TEXT NOT NULL
    """
    parent_stores = [MemberProfile(), Contact()]

class Registered(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    activation_key TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT NOT NULL UNIQUE,
    ipaddr inet
    """

class Session(PGStore):
    create_sql = """
    token TEXT NOT NULL,
    user_id integer NOT NULL UNIQUE,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    last_seen TIMESTAMP WITHOUT TIME ZONE
    """

class UserRole(PGStore):
    create_sql = """
    user_id integer NOT NULL,
    context integer NOT NULL,
    role TEXT NOT NULL
    """

class UserPermission(PGStore):
    create_sql = """
    user_id integer NOT NULL,
    context integer NOT NULL,
    permission TEXT NOT NULL
    """

class BizplaceProfile(PGStore):
    create_sql = """
    short_description TEXT,
    long_description TEXT,
    tags TEXT[],
    website TEXT,
    blog TEXT,
    twitter TEXT[2],
    facebook TEXT[2],
    linkedin TEXT[2],
    booking_email TEXT,
    host_email TEXT
    """

class BizPlace(PGStore):
    create_sql = """
    id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    enabled BOOLEAN DEFAULT True,
    hidden BOOLEAN DEFAULT False,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    langs TEXT[],
    tz TEXT,
    holidays smallint[],
    default_tariff INTEGER,
    currency TEXT,
    logo TEXT
    """
    parent_stores = [BizplaceProfile(), Contact()]

class Request(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    state INTEGER default 1 NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    acted TIMESTAMP WITHOUT TIME ZONE,
    requestor_id integer,
    note TEXT,
    status smallint default 0 NOT NULL,
    approver_id integer,
    api TEXT NOT NULL,
    params bytea
    """
    pickle_cols = ['params']

class RequestPermission(PGStore):
    create_sql = """
    request INTEGER NOT NULL,
    permission TEXT NOT NULL
    """

class Resource(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    enabled BOOLEAN DEFAULT True,
    hidden BOOLEAN DEFAULT False,
    host_only BOOLEAN DEFAULT False,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    type TEXT,
    owner INTEGER NOT NULL,
    short_description TEXT,
    long_description TEXT,
    calc_mode INTEGER,
    picture TEXT,
    archived BOOLEAN DEFAULT False,
    follow_owner_taxes BOOLEAN DEFAULT True,
    taxes BYTEA,
    accnt_code TEXT
    """
    pickle_cols = ['taxes']

class Membership(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    member_id INTEGER NOT NULL,
    tariff_id INTEGER NOT NULL,
    tariff_name TEXT,
    starts DATE NOT NULL,
    ends DATE,
    bizplace_id INTEGER NOT NULL,
    bizplace_name TEXT
    """

class ResourceRelation(PGStore):
    # resourceA --relation--> resourceB
    create_sql = """
    owner INTEGER NOT NULL,
    resourceA INTEGER,
    relation BOOLEAN,
    resourceB INTEGER
    """

class Pricing(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    plan INTEGER NOT NULL,
    resource INTEGER NOT NULL,
    starts DATE,
    ends DATE,
    amount NUMERIC(16, 2) NOT NULL
    """

class Usage(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    resource_id INTEGER,
    resource_name TEXT,
    resource_owner INTEGER NOT NULL,
    notes TEXT,
    quantity REAL,
    calculated_cost NUMERIC(16, 2),
    cost NUMERIC(16, 2),
    total NUMERIC(16, 2),
    tax_dict BYTEA,
    invoice INTEGER,
    start_time  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_time  TIMESTAMP WITHOUT TIME ZONE,
    member INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    pricing INTEGER,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    cancelled_against INTEGER DEFAULT NULL,
    usages_contained INTEGER[],
    usages_suggested INTEGER[],
    name TEXT,
    description TEXT,
    public BOOLEAN DEFAULT false,
    repetition_id INTEGER,
    no_of_people INTEGER
    """
    pickle_cols = ['tax_dict']

class Invoice(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    number INTEGER UNIQUE,
    member INTEGER,
    issuer INTEGER,
    usages INTEGER[],
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    sent TIMESTAMP WITHOUT TIME ZONE,
    invoicee_details bytea,
    total NUMERIC(16, 2),
    tax_dict bytea,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    state INTEGER default 0 NOT NULL,
    notice TEXT,
    po_number TEXT
    """
    #end is keyword, thats why start_date & end_date is used instead of start & end.
    pickle_cols = ['invoicee_details', 'tax_dict']

class InvoicePref(PGStore):
    table_name = "invoice_pref"
    create_sql = """
    owner INTEGER UNIQUE,
    email_text TEXT,
    freetext1 TEXT,
    freetext2 TEXT,
    payment_terms TEXT,
    due_date INTEGER,
    bcc_email TEXT,
    bank_details TEXT,
    company_no TEXT,
    logo TEXT,
    tax_included BOOLEAN DEFAULT False,
    taxes BYTEA,
    taxation_no TEXT,
    start_number INTEGER,
    mode INTEGER NOT NULL,
    billto INTEGER,
    details BYTEA
    """
    pickle_cols = ['details', 'taxes']

class Activity(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    actor INTEGER NOT NULL,
    data BYTEA NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL
    """
    pickle_cols = ['data']

class ActivityAccess(PGStore):
    create_sql = """
    a_id INTEGER NOT NULL,
    role_ctx INTEGER,
    role_name TEXT,
    member_id INTEGER
    """

class OidGen(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    type TEXT NOT NULL,
    PRIMARY KEY(id, type)
    """

class MessageCust(PGStore):
    create_sql = """
    name TEXT NOT NULL,
    owner INTEGER NOT NULL,
    content TEXT NOT NULL,
    lang TEXT
    """

class TaxExemption(PGStore):
    table_name = 'tax_exemption'
    create_sql = """
    member INTEGER NOT NULL,
    issuer INTEGER NOT NULL
    """

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
    id SERIAL NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    state INTEGER default 1 NOT NULL
    """

class Contact(PGStore):
    table_name = "contact"
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    address TEXT,
    city TEXT,
    country TEXT,
    pincode TEXT,
    phone TEXT,
    mobile TEXT,
    fax TEXT,
    email TEXT NOT NULL,
    skype TEXT,
    sip TEXT
    """

class MemberPref(PGStore):
    table_name = "member_pref"
    create_sql = """
    member INTEGER NOT NULL,
    theme TEXT DEFAULT 'default',
    language TEXT DEFAULT 'en'
    """

class BillingPref(PGStore):
    table_name = "billing_pref"
    create_sql = """
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    country TEXT,
    pincode TEXT,
    phone TEXT,
    mobile TEXT,
    fax TEXT,
    email TEXT,
    company_no TEXT
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
    first_name TEXT NOT NULL,
    last_name TEXT,
    display_name TEXT,
    short_description TEXT,
    long_description TEXT,
    interests TEXT[],
    expertise TEXT[],
    website TEXT,
    blog TEXT,
    twitter TEXT[2],
    facebook TEXT[2],
    linkedin TEXT[2],
    use_gravtar BOOLEAN default false,
    organization TEXT
    """

# Container objects
class Member(PGStore):
    table_name = "member"
    create_sql = """
    id INTEGER NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    state INTEGER default 1 NOT NULL
    """
    parent_stores = [MemberProfile(), Contact()]

class Registered(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    activation_key TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT NOT NULL,
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
    role TEXT NOT NULL
    """

class UserPermission(PGStore):
    create_sql = """
    user_id integer NOT NULL,
    permission TEXT NOT NULL
    """

class BizProfile(PGStore):
    create_sql = """
    short_description TEXT,
    long_description TEXT,
    tags TEXT[],
    website TEXT,
    blog TEXT,
    twitter TEXT[2],
    facebook TEXT[2],
    linkedin TEXT[2]
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
    linkedin TEXT[2]
    """

#class BizInvoicingPref(PGStore):
#    invoice_logo = Attribute()
#
class Biz(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    state INTEGER default 1 NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    logo TEXT,
    contact INTEGER
    """
    parent_stores = [BizProfile(), Contact()]

class BizPlace(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    biz INTEGER,
    name TEXT NOT NULL,
    state INTEGER default 1 NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    contact INTEGER,
    langs TEXT[],
    tz TEXT,
    holidays smallint[],
    default_plan INTEGER,
    taxes BYTEA,
    currency TEXT,
    bank_details TEXT
    """
    parent_stores = [BizplaceProfile(), Contact()]
    pickle_cols = ['taxes']

class Request(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    acted_at TIMESTAMP WITHOUT TIME ZONE,
    requestor_id integer,
    request_note TEXT,
    status smallint default 0 NOT NULL,
    approver_id integer,
    approver_perm TEXT NOT NULL,
    _req_data bytea
    """

class Plan(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    bizplace integer NOT NULL,
    description TEXT,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    state INTEGER default 1 NOT NULL
    """

class Subscription(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    subscriber_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    plan_name TEXT,
    starts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ends TIMESTAMP WITHOUT TIME ZONE,
    bizplace_id INTEGER NOT NULL,
    bizplace_name TEXT
    """

class Resource(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    type TEXT,
    state INTEGER default 1 NOT NULL,
    owner TEXT NOT NULL,
    short_description TEXT,
    long_description TEXT,
    time_based BOOLEAN DEFAULT True,
    quantity_unit TEXT
    """

class ResourceRelation(PGStore):
    # resourceA --relation--> resourceB
    create_sql = """
    resourceA INTEGER,
    relation INTEGER,
    resourceB INTEGER
    """

class Pricing(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    plan INTEGER NOT NULL,
    resource INTEGER NOT NULL,
    starts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ends TIMESTAMP WITHOUT TIME ZONE,
    amount NUMERIC(16, 2),
    state INTEGER default 1 NOT NULL
    """

class Usage(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    resource_id INTEGER,
    resource_name TEXT,
    rate REAL,
    quantity REAL,
    calculated_cost NUMERIC(16, 2),
    cost NUMERIC(16, 2),
    tax_dict bytea,
    invoice INTEGER,
    start_time  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_time  TIMESTAMP WITHOUT TIME ZONE,
    member INTEGER NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL
    """
    #price INTEGER NOT NULL,
    pickle_cols = ['tax_dict']

class Invoice(PGStore):
    create_sql = """
    id SERIAL NOT NULL UNIQUE,
    number INTEGER UNIQUE,
    member INTEGER,
    issuer TEXT,
    usages INTEGER[],
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    sent TIMESTAMP WITHOUT TIME ZONE,
    invoicee_details bytea,
    cost NUMERIC(16, 2),
    tax_dict bytea,
    start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    state INTEGER default 0 NOT NULL,
    notice TEXT,
    po_number TEXT
    """
    pickle_cols = ['invoicee_details', 'tax_dict']

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
    role TEXT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL
    """

import datetime
import commonlib.shared.states
import be.repository.access as dbaccess

user_store = dbaccess.stores.user_store
member_store = dbaccess.stores.member_store
contact_store = dbaccess.stores.contact_store
profile_store = dbaccess.stores.memberprofile_store
memberpref_store = dbaccess.stores.memberpref_store

def new(username, password, email, first_name, state=None, language='en', last_name=None, display_name=None, address=None, city=None, country=None, pincode=None, homephone=None, mobile=None, fax=None, skype=None, sip=None, website=None, short_description=None, long_description=None, twitter=None, facebook=None, blog=None, linkedin=None, use_gravtar=None):

    if not display_name: display_name = first_name + ' ' + (last_name or '')
    created = datetime.datetime.now()
    if state is None: state = commonlib.shared.states.member.enabled

    data = dict(username=username, password=password, state=state)
    user_id = user_store.add(data)
    member_ref = member_store.ref(user_id)

    data = dict(owner=member_ref, email=email, address=address, city=city, country=country, pincode=pincode, homephone=homephone, mobile=mobile, fax=fax, skype=skype, sip=sip)
    contact_id = contact_store.add(data)

    data = dict(member=user_id, first_name=first_name, last_name=last_name, display_name=display_name, short_description=short_description, long_description=long_description, website=website, twitter=twitter, facebook=facebook, blog=blog, linkedin=linkedin, use_gravtar=use_gravtar)
    profile_store.add(data)

    data = dict(member=user_id, language=language)
    memberpref_store.add(data)

    data = dict(id=user_id, contact=contact_id, created=created)
    member_store.add(data)

    search_d = dict(id=user_id, display_name=display_name, short_description=short_description, long_description=long_description, username=username)
    #searchlib.add(search_d)
    return user_id

def update(member_id, mod_data):
    member = dbaccess.Member(member_id)
    for attr, value in mod_data.items():
        setattr(member, attr, value)

def delete(member_id):
    member_store.remove(member_id)

def list(): pass

def info(member_id): pass

def details(member_id): pass

def search(): pass

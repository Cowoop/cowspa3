import datetime
import commonlib.shared.states
import be.repository.access as dbaccess
import bases.app
import commonlib.helpers as helpers

user_store = dbaccess.stores.user_store
member_store = dbaccess.stores.member_store
contact_store = dbaccess.stores.contact_store
profile_store = dbaccess.stores.memberprofile_store
memberpref_store = dbaccess.stores.memberpref_store

class MemberCollection:
    def new(self, username, password, email, first_name, state=None, language='en', last_name=None, display_name=None, interests=None, expertise=None, address=None, city=None, country=None, pincode=None, phone=None, mobile=None, fax=None, skype=None, sip=None, website=None, short_description=None, long_description=None, twitter=None, facebook=None, blog=None, linkedin=None, use_gravtar=None):

        if not display_name: display_name = first_name + ' ' + (last_name or '')
        created = datetime.datetime.now()
        if state is None: state = commonlib.shared.states.member.enabled

        data = dict(username=username, password=helpers.encrypt(password), state=state)
        user_id = user_store.add(**data)
        member_ref = member_store.ref(user_id)

        """data = dict(owner=member_ref, email=email, address=address, city=city, country=country, pincode=pincode, phone=phone, mobile=mobile, fax=fax, skype=skype, sip=sip)
        contact_id = contact_store.add(**data)

        data = dict(member=user_id, first_name=first_name, last_name=last_name, display_name=display_name, short_description=short_description, long_description=long_description, website=website, twitter=twitter, facebook=facebook, blog=blog, linkedin=linkedin, use_gravtar=use_gravtar)
        profile_store.add(**data)"""

        data = dict(member=user_id, language=language)
        memberpref_store.add(**data)

        owner = member_store.ref(user_id)
        data = dict(member=user_id, first_name=first_name, last_name=last_name, display_name=display_name, short_description=short_description, long_description=long_description, interests=interests, expertise=expertise, website=website, twitter=twitter, facebook=facebook, blog=blog, linkedin=linkedin, use_gravtar=use_gravtar, id=user_id, owner=owner, email=email, address=address, city=city, country=country, pincode=pincode, phone=phone, mobile=mobile, fax=fax, skype=skype, sip=sip, created=created, state=state)
        member_store.add(**data)

        search_d = dict(id=user_id, display_name=display_name, short_description=short_description, long_description=long_description, username=username)
        #searchlib.add(search_d)
        return user_id

    def delete(self, member_id):
        member_ref = member_store.ref(member_id)
        contact_store.remove_by(owner=member_ref)
        member_store.remove(member_id)
        raise NotImplemented

    def list(self, formember_id, bizplace_ids=[]):
        member = dbaccess.Member(formember_id)
        my_bizplace_ids = [ms.bizplace_id for ms in member.memberships()]
        if bizplace_ids:
            bizplace_ids = set(my_bizplace_ids).intersection(bizplace_ids)
        member_list = []
        for m_dict in dbaccess.find_bizplace_members(bizplace_ids):
            m_dict['id'] = m_dict.pop('member')
            member_list.append(m_dict)
        return member_list

class MemberResource:

    get_attributes = ['state']
    set_attributes = ['state']

    def update(self, member_id, **mod_data):
        member = dbaccess.Member(member_id)
        for attr, value in mod_data.items():
            setattr(member, attr, value)

    def info(self, member_id):
        member = dbaccess.Member(member_id)
        return member.info()

    def details(self, member_id):
        member = dbaccess.Member(member_id)
        return dict(profile=member.profile, contact=member.contact)

    def get(self, member_id, attrname):
        member = dbaccess.Member(member_id)
        return getattr(member, attrname)

    def set(self, member_id, attrname, v):
        member = dbaccess.Member(member_id)
        return setattr(member, attrname, v)

member_resource = MemberResource()
member_collection = MemberCollection()

import datetime
import commonlib.shared.states
import be.repository.access as dbaccess
import bases.app
import commonlib.helpers as helpers
import be.apis.activities as activitylib

user_store = dbaccess.stores.user_store
member_store = dbaccess.stores.member_store
contact_store = dbaccess.stores.contact_store
profile_store = dbaccess.stores.memberprofile_store
memberpref_store = dbaccess.stores.memberpref_store

class MemberCollection:
    def new(self, username, password, email, first_name, state=None, language='en', last_name=None, display_name=None, interests=None, expertise=None, address=None, city=None, country=None, pincode=None, phone=None, mobile=None, fax=None, skype=None, sip=None, website=None, short_description=None, long_description=None, twitter=None, facebook=None, blog=None, linkedin=None, use_gravtar=None):

        if not display_name: display_name = first_name + ' ' + (last_name or '')
        created = datetime.datetime.now()
        if state is None:
            state = commonlib.shared.states.member.enabled
        else:
            state = commonlib.shared.states.member.to_flags(state)

        data = dict(username=username, password=helpers.encrypt(password), state=state) # TODO config salt
        user_id = user_store.add(**data)
        member_ref = member_store.ref(user_id)

        data = dict(member=user_id, language=language)
        memberpref_store.add(**data)

        #owner = member_store.ref(user_id)
        data = dict(member=user_id, first_name=first_name, last_name=last_name, display_name=display_name, short_description=short_description, long_description=long_description, interests=interests, expertise=expertise, website=website, twitter=twitter, facebook=facebook, blog=blog, linkedin=linkedin, use_gravtar=use_gravtar, id=user_id, email=email, address=address, city=city, country=country, pincode=pincode, phone=phone, mobile=mobile, fax=fax, skype=skype, sip=sip, created=created, state=state)
        member_store.add(**data)

        search_d = dict(id=user_id, display_name=display_name, short_description=short_description, long_description=long_description, username=username)
        #searchlib.add(search_d)

        data = dict(name=first_name, location=country, user_id=user_id)
        activity_id = activitylib.add('MemberManagement', 'MemberCreated', user_id, data, created)

        return user_id

    def delete(self, member_id):
        member_ref = member_store.ref(member_id)
        contact_store.remove_by(owner=member_ref)
        member_store.remove(member_id)
        raise NotImplemented

    def list(self, formember_id, bizplace_ids=[]):
        my_bizplace_ids = [ms.bizplace_id for ms in dbaccess.find_memberships(formember_id)]
        if bizplace_ids:
            bizplace_ids = set(my_bizplace_ids).intersection(bizplace_ids)
        member_list = []
        for m_dict in dbaccess.find_bizplace_members(bizplace_ids):
            m_dict['id'] = m_dict.pop('member')
            member_list.append(m_dict)
        return member_list

    def search(self, q, options={'mybizplace': True}, limit=5):
        """
        q: (first or last name or both) or member_id or email or organization. N members whose respective properties starts with provided word (q) where N is limit.
        options:
            mybizplace:
                if True only members having membership in the bizplaces where the current user has membership are returned
                if False membership is not considered
                membership check is not required if current user has admin role
        limit: number of results to return
        return -> list of tuples containing member's display name and member id
        """
        keys = q.split()
        return dbaccess.search_member(keys, options, limit)

class MemberResource:

    get_attributes = ['state']
    set_attributes = ['state']

    def update(self, member_id, **mod_data):
        if 'state' in mod_data:
            mod_data['state'] = commonlib.shared.states.member.to_flags(mod_data['state'])
        member_store.update(member_id, **mod_data)

        data = dict(user_id=member_id, attrs=', '.join(attr for attr in mod_data))
        created = datetime.datetime.now()
        activity_id = activitylib.add('MemberManagement', 'MemberUpdated', member_id, data, created)

    def info(self, member_id):
        info = member_store.get(member_id, ['id', 'state', 'display_name'])
        info['state'] = commonlib.shared.states.member.to_dict(info['state'])
        return info

    def details(self, member_id):
        member_ref = member_store.ref(member_id)
        return dict(profile=memberprofile_store.get_by(member=member_id),
            contact=contact_store.get_by(owner=member_ref))

    def get(self, member_id, attrname):
        if not attrname in self.get_attributes: return
        if attrname == 'state':
            return commonlib.shared.states.member.to_dict(member_store.get(member_id, fields=['state']))
        return member_store.get(member_id, fields=[attrname])

    def set(self, member_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(member_id, **{attrname: v})

member_resource = MemberResource()
member_collection = MemberCollection()

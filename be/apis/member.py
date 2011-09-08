import datetime
import commonlib.shared.constants
import be.repository.access as dbaccess
import bases.app
import commonlib.helpers as helpers
import be.apis.activities as activitylib
import commonlib.shared.static_data as data_lists

user_store = dbaccess.stores.user_store
member_store = dbaccess.stores.member_store
contact_store = dbaccess.stores.contact_store
profile_store = dbaccess.stores.memberprofile_store
memberpref_store = dbaccess.stores.memberpref_store

class MemberCollection:
    def new(self, username, password, email, first_name, state=None, language='English', last_name=None, display_name=None, interests=None, expertise=None, address=None, city=None, country=None, pincode=None, phone=None, mobile=None, fax=None, skype=None, sip=None, website=None, short_description=None, long_description=None, twitter=None, facebook=None, blog=None, linkedin=None, use_gravtar=None ,theme="default"):

        if not display_name: display_name = first_name + ' ' + (last_name or '')
        created = datetime.datetime.now()
        if state is None:
            state = commonlib.shared.constants.member.enabled
        else:
            state = commonlib.shared.constants.member.to_flags(state)

        data = dict(username=username, password=helpers.encrypt(password), state=state) # TODO config salt
        user_id = user_store.add(**data)
        member_ref = member_store.ref(user_id)

        data = dict(member=user_id, language=data_lists.language_map_rev[language], theme=theme)
        memberpref_store.add(**data)

        #owner = member_store.ref(user_id)
        data = dict(member=user_id, first_name=first_name, last_name=last_name, display_name=display_name, short_description=short_description, long_description=long_description, interests=interests, expertise=expertise, website=website, twitter=twitter, facebook=facebook, blog=blog, linkedin=linkedin, use_gravtar=use_gravtar, id=user_id, email=email, address=address, city=city, country=country, pincode=pincode, phone=phone, mobile=mobile, fax=fax, skype=skype, sip=sip, created=created, state=state)
        member_store.add(**data)

        search_d = dict(id=user_id, display_name=display_name, short_description=short_description, long_description=long_description, username=username)
        #searchlib.add(search_d)

        data = dict(name=display_name, id=user_id)
        activity_id = activitylib.add('member_management', 'member_created', data, created)

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

    def search(self, q, options={'mybizplace': False}, limit=5):
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
            mod_data['state'] = commonlib.shared.constants.member.to_flags(mod_data['state'])
        if 'username' in mod_data or 'password' in mod_data:
            mod_data['password'] = helpers.encrypt(mod_data['password'])
            user_store.update(member_id, **mod_data)
        elif 'theme' in mod_data or 'language' in mod_data:
            if 'language' in mod_data:
                mod_data['language'] = data_lists.language_map_rev[mod_data['language']]
            memberpref_store.update_by(dict(member=member_id), **mod_data)
        else:
            member_store.update(member_id, **mod_data)

        display_name = member_store.get(member_id, fields=['display_name'])
        data = dict(id=member_id, name=display_name, attrs=', '.join(attr for attr in mod_data))
        activity_id = activitylib.add('member_management', 'member_updated', data)

    def info(self, member_id):
        info = member_store.get(member_id, ['id', 'state', 'display_name'])
        info['state'] = commonlib.shared.constants.member.to_dict(info['state'])
        return info

    def details(self, member_id):
        member_ref = member_store.ref(member_id)
        profile = profile_store.get_by(dict(member=member_id))[0]
        contact = contact_store.get_by(dict(id=member_id))[0]
        account = dict(username=user_store.get(member_id, ['username']), password="")
        preferences = memberpref_store.get_by(dict(member=member_id), ['theme', 'language'])[0]
        preferences['language'] = data_lists.language_map[preferences['language']]
        memberships = dbaccess.get_member_current_subscriptions(member_id)
        for ms in memberships[::-1]:
            ms['starts'] = ms['starts'].strftime('%b %d, %Y')
            ms['ends'] =  ms['ends'].strftime('%b %d, %Y') if ms['ends'] else '-'
        return dict(profile=profile, contact=contact, account=account, preferences=preferences, memberships=memberships)

    def get(self, member_id, attrname):
        if not attrname in self.get_attributes: return
        if attrname == 'state':
            return commonlib.shared.constants.member.to_dict(member_store.get(member_id, fields=['state']))
        return member_store.get(member_id, fields=[attrname])

    def set(self, member_id, attrname, v):
        if not attrname in self.set_attributes: return
        self.update(member_id, **{attrname: v})

    def get_teriff_history(self, member_id):
        memberships = dbaccess.get_member_teriff_history(member_id)
        for ms in memberships[::-1]:
            ms['starts'] = ms['starts'].strftime('%b %d, %Y')
            ms['ends'] =  ms['ends'].strftime('%b %d, %Y') if ms['ends'] else '-'
        return memberships
        
member_resource = MemberResource()
member_collection = MemberCollection()

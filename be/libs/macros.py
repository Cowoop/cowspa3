import re

import be.repository.stores as stores

# 'biz:{{context:user_biz}}::approve_membership'
# 'biz:{{biz_id_from_plan_id}}::approve_plan'

def has_macro(s):
    return '{{' in s and '}}' in s

def cuser_id(context, data, macro_data):
    return context.user_id

def cuser_perm_names(context, data, macro_data):
    user_id = context.user_id
    return [p.name for p in stores.user_perms_store.get_one_by(user_id=user_id)]

def cuser_biz_ids(context, data, macro_data): # bizplace
    user_id = context.user_id
    member = stores.member_store.get(user_id)
    return member.biz_memberships # bizplace

def bizplace_id_from_plan_id(context, data, macro_data):
    plan_id = data['plan_id']
    plan = stores.plan_store.get(plan_id)
    return str(plan.bizplace_id)

def requestor_display_name(context, data, macro_data):
    user_id = data['requestor_id']
    profile = stores.profilestore.get_one_by(member=user_id, _fields=['display_name'])
    return profile.display_name or stores.userstore.get(user_id).username

def name_from_plan_id(context, data, macro_data):
    plan_id = data['plan_id']
    return stores.plan_store.get(plan_id).name

def id_by_name(context, data, macro_data):
    return stores.permission_store.get_one_by(name=macro_data).id

def extract_from_args(context, data, macro_data):
    return data.get(macro_data)

def extract_from_ctx(context, data, macro_data):
    return getattr(context, macro_data)

processors = dict(
    cuser_id = cuser_id,
    cuser_perm_names = cuser_perm_names,
    cuser_biz_ids = cuser_biz_ids,
    bizplace_id_from_plan_id = bizplace_id_from_plan_id,
    requestor_display_name = requestor_display_name,
    name_from_plan_id = name_from_plan_id,
    id_by_name = id_by_name,
    arg = extract_from_args,
    context = extract_from_ctx
    )

def process(text, context, data):
    macro_pat = '({{[^}]*}})'
    macros = re.findall(macro_pat, text)
    result = text
    for macro in macros:
        macro_name = macro[2:-2]
        if macro_name in data:
            m_result = data[macro_name]
        else:
            macro_data = None
            if ':' in macro_name:
                macro_name, macro_data = macro_name.split(':')
            f = processors[macro_name]
            m_result = f(context, data, macro_data)
        result = result.replace(macro, str(m_result))
    return result

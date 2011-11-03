import itertools
import collections
import datetime
import be.repository.access as dbaccess
import commonlib.shared.roles as roledefs

biz_store = dbaccess.stores.biz_store
bizplace_store = dbaccess.stores.bizplace_store
userrole_store = dbaccess.stores.userrole_store
userpermission_store = dbaccess.stores.userpermission_store

split_context = lambda s: ('', s) if not dbaccess.ctxsep in s else s.split(dbaccess.ctxsep)
add_context = lambda ctx, s: s if not ctx else (str(ctx) + dbaccess.ctxsep + s)

def role_permissions(roles):
    all_perms = []
    for role in roles:
        ctx, role = split_context(role)
        perms = [p.name for p in roledefs.all_roles[role].permissions]
        perms = [add_context(ctx, p) for p in perms]
        all_perms.extend(perms)
    return set(all_perms)

def assign(user_id, roles, context=None):
    if not set(roles).issubset(roledefs.all_roles.keys()):
        raise Exception("Unknown role(s)")
    new_roles = roles
    new_roles = [add_context(context, role) for role in roles]
    existing_roles = (row[0] for row in userrole_store.get_by(crit=dict(user_id=user_id), fields=['role'], hashrows=False))
    roles_to_add = set(new_roles).difference(existing_roles)
    if roles_to_add:
        userrole_store.add_many([dict(user_id=user_id, role=role) for role in roles_to_add])

    # now assign permissions
    perms = role_permissions(roles)
    perms = [add_context(str(context), p) for p in perms]
    existing_perms = (row[0] for row in userpermission_store.get_by(crit=dict(user_id=user_id), fields=['permission'],
        hashrows=False))
    perms_to_add = set(perms).difference(existing_perms)
    if perms_to_add:
        userpermission_store.add_many([dict(user_id=user_id, permission=p) for p in perms_to_add])
    return True

def revoke(user_id, roles, context=None):
    roles = roles
    roles = [add_context(context, role) for role in roles]
    dbaccess.remove_user_roles(user_id, roles)
    # now revoke permissions
    existing_roles = [row[0] for row in userrole_store.get_by(crit=dict(user_id=user_id), fields=['role'], hashrows=False)]
    existing_perms = [row[0] for row in userpermission_store.get_by(crit=dict(user_id=user_id), fields=['permission'], hashrows=False)]
    perms_needed = role_permissions(existing_roles)
    perms_to_add = set(perms_needed).difference(existing_perms)
    perms_to_remove = set(existing_perms).difference(perms_needed)
    print existing_roles, existing_perms, perms_needed, perms_to_add, perms_to_remove
    if perms_to_add:
        userpermission_store.add_many([dict(user_id=user_id, permission=p) for p in perms_to_add])
    if perms_to_remove:
        dbaccess.remove_user_permissions(user_id, perms_to_remove)
    return True

def get_roles(user_id, role_filter=[]):
    """
    role_filter: eg. ['host', 'director']
    returns [{ctx_id: 1, ctx_name: '<name>', roles: ['<role1>', '<role2>']}, ...]
    """
    d = collections.defaultdict(list)
    ctx_name_map = {}
    for row in userrole_store.get_by(crit=dict(user_id=user_id), fields=['role'], hashrows=False):
        ctx_rolename = row[0]
        if dbaccess.ctxsep in ctx_rolename:
            oid, rolename = ctx_rolename.split(dbaccess.ctxsep)
            if rolename in role_filter:
                if oid in ctx_name_map:
                    ctx_name_map[oid].append(rolename)
                else:
                    ctx_name_map[oid] = [rolename]
    return sorted([{'id':oid, 'label':dbaccess.oid2name(oid), 'roles':ctx_name_map[oid]} for oid in ctx_name_map], key=lambda k: k['label'].lower())

def get_user_roles(user_id):
    """
    returns {'Hub Timbaktu': ['Host', 'Director']})
    []
    """
    d = collections.defaultdict(list)
    ctx_name_map = {}
    for row in userrole_store.get_by(crit=dict(user_id=user_id), fields=['role'], hashrows=False):
        # or shall we use sql group by?
        ctx_rolename = row[0]
        if dbaccess.ctxsep in ctx_rolename:
            oid, rolename = ctx_rolename.split(dbaccess.ctxsep)
            if oid in ctx_name_map:
                ctx_name = ctx_name_map[oid]
            else:
                ctx_name = dbaccess.oid2name(oid)
                ctx_name_map[oid] = ctx_name
        else:
            rolename = ctx_rolename
            ctx_name = 'global'
        d[ctx_name].append(roledefs.all_roles[rolename].label)
    return d

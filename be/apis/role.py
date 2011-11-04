import itertools
import collections
import datetime
import be.repository.access as dbaccess
import commonlib.shared.roles as roledefs

bizplace_store = dbaccess.stores.bizplace_store
userrole_store = dbaccess.stores.userrole_store
userpermission_store = dbaccess.stores.userpermission_store

def role_permissions(roles):
    all_perms = []
    for role in roles:
        perms = [p.name for p in roledefs.all_roles[role].permissions]
        all_perms.extend(perms)
    return set(all_perms)

def new_roles(user_id, roles, context):
    """
    Revokes all existing roles (and permissions associated with those roles) and assigns new roles
    new_roles: list
    context: integer. id of the object on which new roles are to be assigned
    """
    new_roles = set(roles)
    # We should try not remove permissions that are common to new_roles and existing_roles that way we ensure that we accidently do not stop 
    # any simultaneously running operation that needs this user's permissions
    if not new_roles.issubset(roledefs.all_roles.keys()):
        raise Exception("Unknown role(s)")
    existing_roles = set(row[0] for row in userrole_store.get_by(dict(user_id=user_id, context=context), fields=['role'], hashrows=False))
    existing_perms = [row[0] for row in userpermission_store.get_by(dict(user_id=user_id, context=context), ['permission'], False)]
    roles_to_grant = new_roles.difference(existing_roles)
    roles_to_revoke = existing_roles.difference(new_roles)
    new_perms = role_permissions(new_roles)
    perms_to_grant = set(new_perms).difference(existing_perms)
    perms_to_revoke = set(existing_perms).difference(new_perms)
    if roles_to_grant:
        userrole_store.add_many([dict(user_id=user_id, role=role, context=context) for role in roles_to_grant])
    if perms_to_grant:
        userpermission_store.add_many([dict(user_id=user_id, permission=p, context=context) for p in perms_to_grant])
    if roles_to_revoke:
        dbaccess.remove_user_roles(user_id, roles_to_revoke, context)
    if perms_to_revoke:
        dbaccess.remove_user_permissions(user_id, perms_to_revoke, context)

def get_roles_in_context(user_id, context):
    """
    role_filter: eg. ['host', 'director']
    returns [{id: 1, label: '<name>', roles: ['<role1>', '<role2>']}, ...]
    """
    return tuple(row[0] for row in dbaccess.userrole_store.get_by(dict(user_id=user_id, context=context), ['role'], False))

def get_roles(user_id, role_filter=[]):
    """
    role_filter: eg. ['host', 'director']
    returns [{id: 1, label: '<name>', roles: ['<role1>', '<role2>']}, ...]
    """
    ctx_roles = collections.defaultdict(list)
    for (role, context) in dbaccess.userrole_store.get_by(dict(user_id=user_id), ['role', 'context'], False):
        if not role_filter or role in role_filter: ctx_roles[context].append(role)
    sorter = lambda d: d['label']
    return sorted((dict(label=dbaccess.oid2name(ctx), id=ctx, roles=roles) for ctx, roles in ctx_roles.items()), key=sorter)

"""
role and permissions

eg. Host at location with id 3 and global admin role
    0 indicates 'global' context

context role
 3      host
 0      admin
"""
import itertools
import collections
import datetime
import be.repository.access as dbaccess
import commonlib.shared.roles as roledefs

bizplace_store = dbaccess.stores.bizplace_store
userrole_store = dbaccess.stores.userrole_store
userpermission_store = dbaccess.stores.userpermission_store
member_store = dbaccess.stores.member_store

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

def remove_roles(user_id, context):
    dbaccess.remove_all_roles_for_user(user_id, context)

def get_roles_in_context(user_id, context):
    """
    returns [{id: 1, label: '<name>', roles: ['<role1>', '<role2>']}, ...]
    """
    return tuple(row[0] for row in dbaccess.userrole_store.get_by(dict(user_id=user_id, context=context), ['role'], False))

def get_roles(user_id=None, role_filter=[]):
    """
    role_filter: eg. ['host', 'director']
    returns [{context: 1, label: '<name>', roles: [{role:'<role1>', label:<label1>, order: <int>}, {role:'<role2>', ..}, ...], ...]
    order: <int> higher the order value lower are the permissions to that role
    """
    if user_id is None:
        user_id = env.context.user_id
    ctx_roles = collections.defaultdict(list)
    # TODO : roles should be list dicts containing role names and role labels
    memberships = dbaccess.get_member_current_memberships(user_id)
    member_roles = [('member', membership.bizplace_id) for membership in memberships]
    team_roles = dbaccess.userrole_store.get_by(dict(user_id=user_id), ['role', 'context'], False)
    all_roles = team_roles + member_roles
    for (role, context) in all_roles:
        if not role_filter or role in role_filter:
            label = roledefs.all_roles[role].label
            order = roledefs.ordered_roles.index(role)
            ctx_roles[context].append(dict(label=label, role=role, order=order))
    sorter = lambda d: d['label']
    role_sorter = lambda d: d['order']
    return sorted((dict(label=dbaccess.oid2name(ctx), context=ctx, roles=sorted(roles, key=role_sorter)) \
        for ctx, roles in ctx_roles.items()), key=sorter)

def get_permissions(user_id):
    return dbaccess.userpermission_store.get_by(dict(user_id=user_id), ['context', 'permission'], hashrows=False)

def get_team(context):
    """
    returns all entries having role defined for that context
    """
    user_ids = set(row[0] for row in dbaccess.userrole_store.get_by(dict(context=context), ['user_id'], hashrows=False))

    result = []
    for id in user_ids:
        d = dict(id=id)
        d['name'] = member_store.get(id, 'name')
        d['roles'] = get_roles_in_context(id, context)
        if not d['roles'] == ['member']:
            result.append(d)

    return result

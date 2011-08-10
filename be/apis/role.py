import itertools
import datetime
import be.repository.access as dbaccess
import commonlib.shared.roles as roledefs

biz_store = dbaccess.stores.biz_store
bizplace_store = dbaccess.stores.bizplace_store
userrole_store = dbaccess.stores.userrole_store
userpermission_store = dbaccess.stores.userpermission_store

def assign(user_id, roles, context=None):
    if not set(roles).issubset(roledefs.all_roles.keys()):
        raise Exception("Unknown role(s)")
    new_roles = roles
    if context:
        new_roles = [(context + '::' + role) for role in roles]
    existing_roles = (row[0] for row in userrole_store.get_by(crit=dict(user_id=user_id), fields=['role'], hashrows=False))
    roles_to_add = set(new_roles).difference(existing_roles)
    if roles_to_add:
        userrole_store.add_many([dict(user_id=user_id, role=role) for role in roles_to_add])

    # now assign permissions
    perms = itertools.chain(*([p.name for p in roledefs.all_roles[role].permissions] for role in roles))
    if context:
        perms = [(context + '::' + p) for p in perms]
    existing_perms = (row[0] for row in userpermission_store.get_by(crit=dict(user_id=user_id), fields=['permission'],
        hashrows=False))
    perms_to_add = set(perms).difference(existing_perms)
    if perms_to_add:
        userpermission_store.add_many([dict(user_id=user_id, permission=p) for p in perms_to_add])
    return True

def revoke(user_id, roles, context=None):
    rolename = role
    if context:
        rolename = context + '::' + role
    dbaccess.remove_user_roles(user_id, roles)
    # now revoke permissions
    return True

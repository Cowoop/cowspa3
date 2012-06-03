"""
common paramaters
-----------------
perms: [(ctx, name), (ctx, name), ..]
ctx:
    int: context_id
    None: current context

usage
-----
from accesscontrol import permissions, roles, AND, OR, NOT, TRUE

def some_api():
    return result

some_api.acl = AND(permissions.has('access_stats'), roles.any('host', 'director'))

some_other_api.acl = NOT(roles.only('member'))

another_api.acl = AND(permissions.any('view', 'list'))
"""

__all__ = ('AND', 'OR', 'NOT', 'HAS_ROLES', 'ANY_ROLE', 'ONLY_ROLE', 'HAS_PERMS', 'ANY_PERM', 'ONLY_ROLE', 'Authenticated', 'Anonymous')

class Condition(object):
    def __init__(self, *checks):
        """
        """
        self.checks = checks

    def __call__(self):
        raise NotImplemented

class ACCondition(Condition):
    def __init__(self, names, context_id=None):
        self.names = names if isinstance(names, (list, tuple)) else (names,)
        self._context_id = context_id

    @property
    def context_id(self):
        return env.context.id if self._context_id is None else self._context_id

    @property
    def contexted_names(self):
        context_id = self.context_id
        return set((context_id, name) for name in self.names)

class HAS_ROLES(ACCondition):
    """
    """
    def __call__(self):
        if self.context_id in env.context.current_roles:
            return bool(env.context.current_roles[self.context_id].role_names.issuperset(self.names))
        return False

class ANY_ROLE(ACCondition):
    """
    """
    def __call__(self):
        if self.context_id in env.context.current_roles:
            return bool(env.context.current_roles[self.context_id].role_names.intersection(self.names))
        return False

class ONLY_ROLE(ACCondition):
    """
    """
    def __call__(self):
        return env.context.current_roles[self.context_id].role_names == self.names

class HAS_PERMS(ACCondition):
    """
    """
    def __call__(self):
        print(self.contexted_names)
        print(env.context.current_perms)
        return bool(env.context.current_perms.issuperset(self.contexted_names))

class ANY_PERM(ACCondition):
    """
    """
    def __call__(self):
        return bool(env.context.current_perms.intersection(self.contexted_names))

class ONLY_PERM(ACCondition):
    """
    """
    def __call__(self):
        return env.context.current_perms == self.contexted_names

class AND(Condition):
    """
    """
    def __call__(self):
        return all(check() for check in self.checks)

class OR(Condition):
    """
    """
    def __call__(self):
        return any(check() for check in self.checks)

class NOT(Condition):
    """
    """
    def __call__(self):
        return not self.checks[0]()

class Authenticated(Condition):
    def __call__(self):
        return hasattr(env.context, 'user_id')

class Anonymous(Condition):
    def __call__(self):
        return True

def is_host():
    condition = HAS_ROLES('host')
    return condition()

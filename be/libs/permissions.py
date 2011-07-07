import macros
import be.repository.stores as stores

# Resource:{{ARG:resource_id}}::owner
# Biz:{{ARG:biz_id}}::owner
# Biz:{{ARG:biz_id}}::manage_resources
# manage_own_profile
# Profile:{{CONTEXT:user_id}}::
# 
# EQ('{{current_user_id}}', '{{ARG:member_id}}')
# match_cuser('{{ARG:member_id}}')
# HAS('some_permission')
# is_host_of('{{ARG:member_id}}')
# AND(is_host_of('{{ARG:member_id}}'), HAS('some_permission'))

class Check(object): pass

class OR(Check):
    def __init__(self, *checks):
        self.checks = checks
    def __call__(self, context, kw):
        for check in self.checks:
            if check(context, kw):
                return True
        return False

class AND(Check):
    def __init__(self, *checks):
        self.checks = checks
    def __call__(self, context, kw):
        for check in self.checks:
            if not check(context, kw):
                return False
        return True

class EQ(Check):
    def __init__(self, s1, s2):
        self.strings = (s1, s2)
    def __call__(self, context, kw):
        s1, s2 = self.strings
        if macros.has_macro(s1):
            s1 = macros.process(s1, context, kw)
        if macros.has_macro(s2):
            s1 = macros.process(s2, context, kw)
        return s1 == s2

class MatchCUser(Check):
    def __init__(self, s1):
        self.s1 = s1
    def __call__(self, context, kw):
        s1 = macros.process(self.s1, context, kw)
        return s1 == str(context.user_id)

class HostOfMember(Check):
    def __init__(self, member_str):
        self.member_str = member_str
    def __call__(self, context, kw):
        if macros.has_macro(member_str):
            member_str = macros.process(self.member_str, context, kw)
        member_id = int(member_str)


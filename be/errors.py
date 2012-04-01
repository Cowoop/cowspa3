class ErrorWithHint(Exception):
    def __init__(self, hints):
        self.hints = hints if isinstance(hints, (tuple, list)) else (hints,)

class APIExecutionError(Exception):
    def __init__(self, code, msg, data={}):
        self.code = code
        self.msg = msg
        self.data = data

class SecurityViolation(Exception):
    def __init__(self, msg):
        self.msg = msg

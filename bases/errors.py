success = 0
invalid_api = 1
uncaught_exception = 13

class APIExecutionError(Exception):
    def __init__(self, retcode, result): pass

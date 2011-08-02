class ErrorWithHint(Exception):
    def __init__(self, hints):
        self.hints = hints if isinstance(hints, (tuple, list)) else (hints,)

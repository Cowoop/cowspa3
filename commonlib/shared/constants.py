import commonlib.helpers

Constants = commonlib.helpers.Constants

class states(Constants):
    """
    class mystates(states):
        names = ['enabled', 'hidden']

    mystates.enabled
    mystates.hidden
    mystates.to_flags(dict(enabled=True)) -> 1
    mystates.to_flags(dict(hidden=True)) -> 2
    mystates.to_flags(dict(enabled=True, hidden=True)) -> 3
    mystates.to_dict(3) -> dict(enabled=True, hidden=True)
    mystates.to_dict(2) -> dict(enabled=False, hidden=True)
    """
    names = ['enabled', 'hidden']

    def to_dict(self, state_flag):
        state_dict = dict((state, bool(state_flag & getattr(self, state))) for state in self.names)
        return state_dict

    def to_flags(self, state_dict):
        state_flag = 0
        for state in state_dict:
            state_flag = state_flag | (getattr(self, state) * int(state_dict[state]))
        return state_flag

class user(states): pass

class member(states): pass

class resource(states):
    names = ['enabled', 'host_only', 'repairs']

member = member()
resource = resource()

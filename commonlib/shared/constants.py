import commonlib.helpers

Constants = commonlib.helpers.Constants

class states(Constants):
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

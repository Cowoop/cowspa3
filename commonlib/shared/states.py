class states(object):
    enabled = 0
    hidden = 1
    
    @classmethod
    def to_dict(self, state_flag):
        attrs = (state for state in dir(self) if state[0] != '_' and not callable(getattr(self, state)))
        state_dict = dict((state, bool(state_flag & (2 ** getattr(self, state)) )) for state in attrs)
        return state_dict
        
    @classmethod
    def to_flags(self, state_dict):
        state_flag = 0
        for state in state_dict:
            state_flag = state_flag | (( 2 ** getattr(self, state) * int(state_dict[state])))
        return state_flag
        
class member(states): pass

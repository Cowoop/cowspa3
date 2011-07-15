class states(object):
    disabled = 0
    enabled = 1
    hidden = 2
    
    def to_dict(self, state_flag):
        state_dict = dict(
            enabled = bool(state_flag & self.enabled),
            hidden  = bool(state_flag & self.hidden))
        return state_dict
        
    def to_flags(self, state_dict):
        state_flag = 0
        if state_dict['enabled']:
            state_flag = state_flag | self.enabled
        if state_dict['hidden']:
            state_flag = state_flag | self.hidden
        return state_flag
        
class member(states): pass

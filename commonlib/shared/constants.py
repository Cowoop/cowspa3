import commonlib.helpers

Constants = commonlib.helpers.Constants

class states(Constants):
    names = ['enabled', 'hidden']

    def to_dict(self, state_flag):
        state_dict = dict((state, bool(state_flag & (2 ** getattr(self, state)) )) for state in self.names)
        return state_dict

    def to_flags(self, state_dict):
        state_flag = 0
        for state in state_dict:
            state_flag = state_flag | (( 2 ** getattr(self, state) * int(state_dict[state])))
        return state_flag

class member(states): pass

class resource_relations(Constants):
    names = ['contains', 'contains_opt', 'requires', 'suggests']

member = member()
resource_relations = resource_relations()

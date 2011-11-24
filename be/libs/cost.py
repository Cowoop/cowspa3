import decimal
import itertools
import datetime

import commonlib.helpers
import be.repository.access as dbaccess

odict = commonlib.helpers.odict

def to_decimal(n):
    return decimal.Decimal(str(n)).quantize(decimal.Decimal('.00'))

class flags:
    proceed = 0
    stop = 1

class Cost(object):
    def __init__(self):
        self.records = [('Start', 0)]
    def last(self):
        rec = self.records[-1:]
        if rec: return rec[0][1]
    def new(self, stage, amount):
        self.records.append((stage, amount))

class Rule(object):
    name = "Base Rule"
    def apply(self, env, usage, cost):
        """
        must return one of the flags
        """
        raise NotImplemented

class Processor(object):
    def __init__(self, usage, rules):
        self.usage = usage
        self.rules = rules
        self.cost = Cost()
        self.shared = {} # later we may consider making shared immutable for existing keys
    def run(self):
        for rule in self.rules:
            flag = rule.apply(self.shared, self.usage, self.cost)
            if flag == flags.stop:
                break
        return self.cost.last()

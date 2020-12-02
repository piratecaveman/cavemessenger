import re


class BaseRule(object):
    def __init__(self, name: str, pattern: str, replacement: str = None):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement

    @property
    def compiled(self) -> re.compile:
        return re.compile(self.pattern, re.IGNORECASE)


class RuleBook(object):
    rules = {
        'c_hard': BaseRule(name='c_hard', pattern=r'c([^ieyh])', replacement=r'k\1'),
        'c_soft': BaseRule(name='c_soft', pattern=r'c(i|e|y)', replacement=r's\1'),
        'th': BaseRule(name='th', pattern=r'th', replacement=r'z'),
        'ph': BaseRule(name='ph', pattern=r'ph', replacement=r'f'),
        'tion': BaseRule(name='tion', pattern=r'tion', replacement=r'shun'),
        'sion': BaseRule(name='sion', pattern=r'sion', replacement=r'shun'),
        'ould': BaseRule(name='ould', pattern=r'ould', replacement=r'ud'),
        'tood': BaseRule(name='tood', pattern=r'tood', replacement=r'tud'),
        'ter': BaseRule(name='ter', pattern=r'ter', replacement=r'tr'),
        'der': BaseRule(name='der', pattern=r'der', replacement=r'dr'),
        'ted': BaseRule(name='ted', pattern=r'ted', replacement=r'td'),
        'des': BaseRule(name='des', pattern=r'des', replacement=r'ds'),
        'bed': BaseRule(name='bed', pattern=r'bed(?<=\b)', replacement=r'bd'),
        'repeated': BaseRule(name='repeated', pattern=r'([a-z])\1', replacement=r'\1'),
        'trailing_e': BaseRule(name='trailing_e', pattern=r'([a-z]{3,})e\b', replacement=r'\1')
    }

    def __init__(self):
        self.generate_rules()

    def generate_rules(self):
        for key in RuleBook.rules.keys():
            self.__setattr__(key, self.rules[key])

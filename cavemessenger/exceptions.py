from cavemessenger.rules import BaseRule


class BaseExceptionPass(object):
    def __init__(self, name: str, word: str, replacement: str = None, rule: BaseRule = None):
        self.name = name
        self.word = word
        self.replacement = replacement
        self.rule = rule

    @property
    def is_replaceable(self):
        if self.replacement is None:
            return False
        return True

    @property
    def is_static(self):
        if 'static' in self.name:
            return True
        return False


class StaticPass(BaseExceptionPass):
    def __init__(self, word: str):
        BaseExceptionPass.__init__(self, name='static', word=word, replacement=None, rule=None)


class StaticReplacementPass(BaseExceptionPass):
    def __init__(self, word: str, replacement: str):
        BaseExceptionPass.__init__(self, name='static_replacement', word=word, replacement=replacement, rule=None)


class RulePass(BaseExceptionPass):
    def __init__(self, word: str, rule: BaseRule):
        BaseExceptionPass.__init__(self, name='rule', word=word, replacement=None, rule=rule)


class RuleReplacementPass(BaseExceptionPass):
    def __init__(self, word: str, rule: BaseRule, replacement: str):
        BaseExceptionPass.__init__(self, name='rule_replacement', word=word, replacement=replacement, rule=rule)


class ExceptionPass(object):
    static = StaticPass
    static_replacement = StaticReplacementPass
    rule = RulePass
    rule_replacement = RuleReplacementPass

    def __init__(self):
        pass

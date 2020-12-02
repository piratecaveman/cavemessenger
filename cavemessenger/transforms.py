import re

from cavemessenger.rules import RuleBook
from cavemessenger.rules import BaseRule
from cavemessenger.exceptions import ExceptionPass


class Transformer(object):
    def __init__(self):
        self.exceptions = {
            'here': ExceptionPass.static('here'),
            'took': ExceptionPass.static_replacement('took', 'tuk'),
            'through': ExceptionPass.rule('through', rule=BaseRule(name='th', pattern=r'th'))
        }

    def germanize(self, text: str):

        word_list = text.split(' ')
        processed_word_list = list()

        for word in word_list:
            working_copy = word
            if word.startswith('@'):
                processed_word_list.append(word)
                continue

            for key in RuleBook.rules.keys():
                if working_copy.lower() not in self.exceptions.keys():
                    working_copy = re.sub(RuleBook.rules[key].compiled, RuleBook.rules[key].replacement, working_copy)
                else:
                    exception = self.exceptions[working_copy.lower()]
                    if exception.is_static:
                        if exception.is_replaceable:
                            working_copy = exception.replacement
                        else:
                            pass
                    else:
                        if exception.rule.name == key:
                            if exception.is_replaceable:
                                working_copy = exception.replacement
                            else:
                                pass
                        else:
                            working_copy = re.sub(
                                RuleBook.rules[key].compiled,
                                RuleBook.rules[key].replacement,
                                working_copy
                            )
            if word[0].isupper():
                working_copy.capitalize()
            processed_word_list.append(working_copy)
        transformed_text = ' '.join(processed_word_list)
        return transformed_text

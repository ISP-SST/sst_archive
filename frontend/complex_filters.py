from functools import reduce

from django.db.models import Q
from pyparsing import infixNotation, opAssoc, Suppress, CharsNotIn, Word, alphas, alphanums, quotedString, removeQuotes, \
    ZeroOrMore, Empty, ParseException


def string_to_python(value):
    if value in ('true', 'True', True):
        value = True
    elif value in ('false', 'False', False):
        value = False
    elif value in ('nil', 'none', 'None', None):
        value = None
    return value


class EmptyFilter:
    """Filter for the empty string"""

    def __init__(self):
        pass

    def __repr__(self):
        return 'EmptyFilter()'

    def as_q(self):
        return Q()


class SimpleFilter:
    """Regular Django filter on field, e.g. id__lt=2"""

    def __init__(self, t):
        self.lookup = t[0]
        self.value = t[1]

    def __repr__(self):
        return 'SimpleFilter(%s=%s)' % (self.lookup, self.value)

    def as_q(self):
        return Q(**{self.lookup: self.python_value})

    @property
    def python_value(self):
        """Convert the string value into a python object"""

        # Split on ',' if not empty string and either an "in" or "range" lookup
        if self.lookup.endswith('__in') or self.lookup.endswith('__range'):
            python_value = self.value.split(',')
        else:
            python_value = string_to_python(self.value)

        return python_value


class BooleanOperator:
    def __init__(self, t):
        self.args = t[0][0::2]

    def __repr__(self):
        sep = ' %s ' % self.reprsymbol
        return '(' + sep.join(map(str, self.args)) + ')'


class AndOperator(BooleanOperator):
    reprsymbol = 'AND'

    def as_q(self):
        return reduce(lambda a, b: a & b.as_q(), self.args, Q())


class OrOperator(BooleanOperator):
    reprsymbol = 'OR'

    def as_q(self):
        return reduce(lambda a, b: a | b.as_q(), self.args, Q())


class NotOperator:
    def __init__(self, t):
        self.arg = t[0][1]

    def __repr__(self):
        return 'NOT ' + str(self.arg)

    def as_q(self):
        return ~self.arg.as_q()


# Parse the empty string
EmptyStringParser = Empty()
EmptyStringParser.setParseAction(EmptyFilter)

# Parse expressions like name=hello or name__contains="hello world"
SimpleExpressionParser = Word(alphas, alphanums + '_') + Suppress('=') + (
        quotedString.setParseAction(removeQuotes) | ZeroOrMore(' ') + CharsNotIn('() '))
SimpleExpressionParser.setParseAction(SimpleFilter)

# Parse complex expressions using "and" "or" "not" and parenthesis
ComplexExpressionParser = infixNotation(SimpleExpressionParser, [
    ('not', 1, opAssoc.RIGHT, NotOperator),
    ('and', 2, opAssoc.LEFT, AndOperator),
    ('or', 2, opAssoc.LEFT, OrOperator)
])

# Parse a any of the above, from longest match to shortest
SearchExpressionParser = ComplexExpressionParser ^ SimpleExpressionParser ^ EmptyStringParser


class InvalidFilterError(Exception):
    pass


def get_complex_filter(search_expression, ignore_bad_filters=False):
    """Parse a complex search expression into a Q filter usable by Django"""
    try:
        parse_result = SearchExpressionParser.parseString(search_expression, parseAll=True)
    except ParseException as why:
        if ignore_bad_filters:
            return Q()
        else:
            raise InvalidFilterError(str(why))
    else:
        return parse_result[0].as_q()

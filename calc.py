import re

"""
EXPRESSION :: = TERM + EXPRESSION | TERM - EXPRESSION | TERM
TERM ::= EXPONENT * TERM | EXPONENT / TERM | EXPONENT
EXPONENT ::= FACTOR ^ EXPONENT | FACTOR | -EXPONENT
FACTOR ::= number | ( EXPRESSION )

(using the convention that ALLCAPS means non-terminal, while `number`
represents [0-9]+(?:.[0-9]+), so all the positive reals)

This grammar generates all the string of valid arithmetic statement.
Since it's right recursive, it's simpler to parse, by using a
recursive descent parser. However, it also means that using this
grammar will force every operator to right-associativity, which is not
always wanted, especially with - and / (which are left-associative),
whereas + and * are associative, so the precedence doesn't matter.
However, if we were to force left-associativity, the results would
look like this:


    (this is a simplified version, with only addition between numbers
    and parenthesized expressions)

    EXPRESSION : EXPRESSION - VALUE | VALUE
    VALUE : NUMBER | ( EXPRESSION )

    def expression(tokens):
        res = expression(tokens) <---  ouch!
        op = tokens[0]
        if op == '-':
            right = value(tokens)
            res = op(res, right)
        return res

which would obviously cause an infinite recursion. To avoid this
problem, we should change the first rule in this way:

     EXPRESSION : VALUE - EXPRESSION | VALUE

However, this cause the - to be right associative. So, for example,
the string 5 - 4 - 1 would be parsed incorrectly as 5 - (4 - 1).
So, we change the function expression:

    def expression(tokens):
        res = value(tokens)
        op = tokens[0]
        while op == '-':
            right = expression(tokens)
            res = op(res, right)
        return res

Yep, curious.

The tokenizer is rather barbarian, however it works, as long as
numbers are not in scientific notation (e.g. 3.4e56 doesn't work)

Functions applications should be added in the exponent() method.

The productions `factor ::= -number | - ( expr )`
are quite tempting, however, they're wrong, because they change the
associativity of the ^ operator. -2^2 = -4, not 4.
To avoid this problem, the right places where productions to handle
negative numbers must be placed is: 1. in fact2, the production ^
-fact1, and in exp1 `-fact1 fact2` should be added. The left recursive
grammar, instead, requires only a new production exponent ::= -exponent.

"""

class Tokenizer(object):
    def __init__(self, string):
        self.regex = re.compile("((\d+(?:\.\d+)?)|([+*/\^-])|([\(\)]))")
        self.string = string.replace(' ', '')

    def tokenize(self):
        result = []
        while self.string:
            try:
                matchobj = re.match(self.regex, self.string)
                match = matchobj.group(1)
            except AttributeError:
                raise Exception("symbol not valid!")
            if (not (match[0].isdigit() or match[-1].isdigit()) 
                and match not in '~+*/^-()'):
                raise Exception("symbol %s is not supported" %match)
            result.append(match)
            self.string = self.string[len(match):]
        return result
    

class Parser(object):
    def __init__(self, tokenization):
        self.tokens = tokenization
        self.current = tokenization[0]

    def next(self):
        self.tokens = self.tokens[1:]
        self.current = self.tokens[0] if len(self.tokens) > 0 else None

    def match(self, char):
        """ Raise error if the current char doesn't match @char """
        assert self.current == char, ("symbol %s is not valid here, "
                                      "expected %s" %(self.current, char))

    def expression(self):
        res = self.term()
        while self.current is not None and self.current in '+-':
            if self.current == '+':
                self.next()
                res += self.term()
            if self.current == '-':
                self.next()
                res -= self.term()
        return res

    def term(self):
        res = self.exponent()
        ## note: some code I found right after the article
        ## `How to write a calculator in python in 70 lines` used a
        ## solution similar to this, but they usually kept two while
        ## loop, one for * and the other for / (the same for + and -),
        ## however, this approach has the flaw that it ignores * after
        ## / and + after -, so an expression like 5 - 2 + 3 would be
        ## evaluated as 5 - 2 = 3, and 10 / 2 * 2 = 2.5
        while self.current is not None and self.current in '*/':
            if self.current == '*':
                self.next()
                res *= self.exponent()
            if self.current == '/':
                self.next()
                res /= self.exponent()
        return res

    def exponent(self):
        if self.current == '-':
             self.next()
             res = -self.exponent()
        else:
            res = self.number()
            while self.current == '^':
                self.next()
                res = res ** self.exponent()
        return res

    def number(self):
        res = None
        if self.current is '(':
            self.next()
            res = self.expression()
            self.match(")")
            self.next()
        elif self.current[0].isdigit():
            res = float(self.current)
            self.next()
        else:
            raise Exception("Not a number")
        return res


while 1:
    t = Tokenizer(raw_input('> '))
    p = Parser(t.tokenize())
    print(p.expression())

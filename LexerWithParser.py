from sly import *


# This is a basic Implementation of a Lexical Analyzer with a Basic Parser.
class BasicLexer(Lexer):
    # These are all the tokens that our language can understand.
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, TO, EQEQ, GRTH, LSTH, FUN, ARROW}
    ignore = '\t '  # This lets us Ignore Tabs and Spaces.

    # These are 1-Character Tokens such as +, -, =, etc...
    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}

    # These are the Keywords we will be using. They are all Regular Experssions.
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'

    # This means that a variable name has to start with a letter or an _
    # The * means you can type any number of letters after the first one.
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # This means that a string can be anything as long as it's between double quotes >> " anything ".
    STRING = r'\".*?\"'

    EQEQ = r'=='
    GRTH = r'>'
    LSTH = r'<'

    # Here we define what a number is.
    # d+ Means that it has to be one or more digits.

    @_(r'\d+')
    def NUMBER(self, t):
        # Here we get a number and convert it to a python number.
        t.value = int(t.value)
        # Here we just return the number.
        return t

    # This is a function for a Comment. A comment starts with #.
    @_(r'#.*')
    def COMMENT(self, t):
        # We just pass as we don't use comments at all in compilation.
        pass

    # This function is for making a new line.
    @_(r'\n+')
    def newline(self, t):
        # If we see a new line, we will increment the line number variable (This variable : lineo)
        # This way, if we get an error, we can tell the user What line has it.
        # We are not using new lines at all, though.
        self.lineno = t.value.count('\n')


# This is a basic Parser Class.
class BasicParser(Parser):
    tokens = BasicLexer.tokens

    # Precendence is used to tell the compiler how to handle mass Equations the correct way.
    # Basically, it handles Multiplication and Division BEFORE Addition and Subtraction.

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    # A parser is made of Grammar Rules.
    # Here is how it understands these rules.



    def __init__(self):
        self.env = {}

    # Here we are saying that a statement can be empty. This is an empty statement :  ( '' )
    @_('')
    def statement(self, p):
        # If it's empty, do nothing.
        pass

    # This is the FOR Loop.
    # It starts with a variable, which is our Counter. It goes up TO an Expression.

    # An Example : FOR i = 0 TO 10 THEN i.
    # What this loop does is, it runs for 10 times and prints the variable i.
    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        #			root		  first child		variable	iteration	2nd child
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    # an IF statement is the IF keyword, followed by a Condition, followed by a THEN, followed by the 2 branches that are executed depending on the condition.
    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        #				root	left branch				right branch
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    # This is the Function.
    # A function is the Keyword FUN, followed by (), Arrow operator and then the statement we want to execute.
    # This is how a function looks like : FUN Hello () -> statement

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    # Here are the conditions.
    # We only have 3 conditions, for Simplicity.

    @_('expr EQEQ expr')  # Equal
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('expr GRTH expr')  # Greater Than
    def condition(self, p):
        return ('condition_GRTH', p.expr0, p.expr1)

    @_('expr LSTH expr')  # Less Than
    def condition(self, p):
        return ('condition_LSTH', p.expr0, p.expr1)

    # Here is how we handle Variable Assignment.
    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    # A variable Assignment can be an Expression.
    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    # A variable Assignment can also be a String.
    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    #	Expressions can be broken down into Many different things.
    @_('expr')
    def statement(self, p):
        return (p.expr)

    # This is an expression made of 2 Expressions with a PLUS between them. ( Expressions + Expression )

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    # This is an expression made of 2 Expressions with a MINUS between them. ( Expressions - Expression )

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    # This is an expression made of 2 Expressions with an ASTERISK between them. ( Expressions * Expression )

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    # This is an expression made of 2 Expressions with a DIVIDE between them. ( Expressions / Expression )

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    # An Expression can be just a variable.
    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    # An Expression can be just a Number.
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)




        # This Segment of the code is for the Lexer only.


'''

if __name__ == '__main__':
    # We create an instance of our Lexical Analyzer.
    lexer = BasicLexer()
    # Taking Input from the user.
    while True:
        try:

            text = input('Lexer >> ')
        except EOFError:
            break
        if text: 	#If the input is okay, we pass it to the Lexer.
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)



    # A statement for Everything :  IF a == 10 THEN a = a * 2 ELSE a = a * 5
'''

# This segment of code is for the Lexer with Parser.
if __name__ == '__main__':

    lexer = BasicLexer()
    # We create an instance of our Parser.
    parser = BasicParser()
    env = {}
    while True:
        try:
            # Taking Input from the user.
            text = input('Parse >> ')
        except EOFError:
            break

        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)


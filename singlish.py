################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-14; See http://norvig.com/lispy.html

################ Types

from __future__ import division

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    try:
        if 'bro' not in s and 'bang' not in s:
            raise SyntaxError('expected (')
        return s.replace('(',' ( ').replace('bang',' ( ').replace('bro',' ( ').replace(')',' ) ').replace('lah',' ) ') \
        .replace('leh',' ) ').replace('ah',' ) ').replace('meh',' ) ').replace('lor',' ) ').split()
    except:
        pass
    

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."

    try:
        # if tokens == None:
        #     return None
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF while reading')
        token = tokens.pop(0)
        # print tokens
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(read_from_tokens(tokens))
            tokens.pop(0) # pop off ')'
            return L
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return atom(token)
    except:
        print "Bang jialat sia. Syntax error. You confirm chop guarantee not from Singapore."

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Environments

def standard_env():
    "An environment with some Scheme standard procedures."
    import math, operator as op
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'seefirst':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal':  op.eq, 
        'length':  len, 
        'with':    lambda *x: list(x), 
        'list':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'dowan':     op.not_,
        'null?':   lambda x: x == [], 
        'number': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
        'abuthen': True,
        'talkcocksingsong': False,
    })
    return env

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

global_env = standard_env()

################ Interaction: A REPL

def start(prompt='Singlish > '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: 
            print(sgtransform(lispstr(val)))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if  isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

def sgtransform(exp):
    if isinstance(exp, bool):
        if exp == True:
            return "Bang abuthen"
        else:
            return "Bang you talkcocksingsong ah"
    return "Bang " + str(exp) + " lah"

################ Procedures

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

def eval(x, env=global_env):
    # print x
    "Evaluate an expression in an environment."
    print x
    if isinstance(x, Symbol):      # variable reference
        try:
            return env.find(x)[x]
        except:
            return x
    elif not isinstance(x, List):  # constant literal
        return x                
    elif len(x) > 1 and x[0] == 'simi' and x[1] == 'si':          # (quote exp)
        (_, _, exp) = x
        return eval(exp, env)    
    elif x[0] == 'gimme':          # (quote exp)
        (_, exp) = x
        return eval(exp, env)
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, _, _, conseq, _, _, _, alt) = x # IF TEST HOR THEN 
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif len(x) > 1 and x[1] == 'is':         # (define var exp)
        try:
            (var, _, exp) = x
            env[var] = eval(exp, env)
        except ValueError:
            print "Tankuku, I catch no ball"
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'given':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # (proc arg...)
        proc = eval(x[1], env)
        if len(x) <= 1:
            y = [x[0]]
        else:
            y = [x[0]] + x[2:]
        args = [eval(exp, env) for exp in y]
        return proc(*args)


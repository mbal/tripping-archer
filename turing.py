#-*- coding: utf-8 -*-
import sys
import time
import operator

def tokenize(expr):
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    return expr.split()

def rep(tokens):
    return t(tokens, 0)

def t(tokens, k):
    if len(tokens) == k:
        raise SyntaxError("Errore! Non posso analizzare il vuoto")
    tok = tokens[k]
    if tok == '(':
        i = k = k+1
        l = []
        while tokens[i] != ')':
            res, n = t(tokens, i) #analizzo ogni token in cui è divisa la stringa
            l.append(res)         #ritorna: una rappresentazione del token e la sua lunghezza
            i = n
        return l, i+1
    elif tok == ')':
        raise SyntaxError(") non attesa")
    else:
        return parse_atom(tok), k+1

def rep2(tokens):
    #uguale alla funzione t(tokens, k) qua sopra
    if len(tokens) == 0:
        raise SyntaxError("Ehi, non mi hai dato nulla!")
    tok = tokens.pop(0)
    if tok == '(':
        p = []
        while tokens[0] != ')':
            p.append(rep2(tokens))
        tokens.pop(0)
        return p
    else:
        return parse_atom(tok)
    return

def parse_atom(t):
    try: 
        return int(t)
    except ValueError:
        try: return float(t)
        except ValueError: return t

def parse(expr):
    return rep(tokenize(expr))[0]

def atom(expr):
    return not isinstance(expr, list)


class Env:
    def __init__(self, params=(), args=(), outer=None):
        self.ambiente = {}
        self.ambiente.update(zip(params, args))
        self.outer = outer

    def find(self, x):
        if x in self.ambiente:
            return self.ambiente
        else:
            return self.outer.find(x)

    def __getitem__(self, x):
        return self.ambiente[x]

    def __setitem__(self, x, y):
        self.ambiente[x] = y

def evaluate(e, environment):
    #print(e)
    if isinstance(e, str):
        return environment.find(e)[e]
    elif not isinstance(e, list):
        return e
    elif e[0] == 'atomo?':
        return atom(evaluate(e[1]), environment) 
    elif e[0] == 'crea':
        return e[1]
    elif e[0] == 'eq?':
        op1 = evaluate(e[1], environment)
        op2 = evaluate(e[2], environment)
        return (op1 == op2) and atom(op1)
    elif e[0] == 'primo':
        #print(e)
        return evaluate(e[1:], environment)[0]
    elif e[0] == 'resto':
        #print(e)
        return evaluate(e[1:], environment)[1:]
    elif e[0] == 'costruisci':
        exp1 = evaluate(e[1], environment)
        exp2 = evaluate(e[2], environment)
        return [exp1] + exp2
    elif e[0] == 'blocco':
        exps = [evaluate(x, environment) for x in e[1:]]
        return exps[-1] #valuta ogni espressione, ma ritorna il valore solo dell'ultima
    elif e[0] == 'null?':
        return evaluate(e[1], environment) == []
    elif e[0] == 'cond':
        for (predicato, expr) in e[1:]:
            if predicato == 'else': #else è sempre vero
                return evaluate(expr, environment)
            if evaluate(predicato, environment):
                return evaluate(expr, environment)
    elif e[0] == 'define':
        name = e[1]
        body = e[2]
        environment[name] = evaluate(body, environment)
    elif e[0] == 'lambda':
        vals = e[1]
        body = e[2]
        #print(vals)
        return lambda *args: evaluate(body, Env(vals, args, environment))
    elif e[0] == 'tempo': 
        start = time.time()  
        r = evaluate(e[1], environment)
        print("%.5f" %(time.time()-start))
        return r
    else:
        exps = [evaluate(exp, environment) for exp in e]
        proc = exps.pop(0)
        try:
            return proc(*exps)
        except TypeError: #questo errore avviene quando proc non è una funzione, ma una lista o un valore booleano.
            return proc

def stampa(arg):
    print(arg)

def create_global_dict():
    #Creiamo l'insieme delle funzioni disponibili nel linguaggio. Potete aggiungere
    #ulteriori funzioni semplicemente aggiungendo un elemento al dizionario, il primo
    #elemento sarà il nome con cui si vuole chiamare in Turing, mentre il secondo è
    #l'operazione associata
    t = Env([], [])
    t.ambiente.update({'+': operator.add,
                       '-': operator.sub,
                       '*': operator.mul,
                       '/': operator.div, 
                       '=': lambda x, y: x == y, 
                       '<': operator.lt, 
                       '>': operator.gt, 
                       'modulo': lambda x, y: x % y, 
                       'stampa' :stampa,
                       'True': True, 'False': False })
    return t

global_env = create_global_dict() 

def prompt():
    while True:
        val = evaluate(parse(raw_input('>>> ')), global_env)
        print(val)

if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    val = evaluate(parse(f.read()), global_env)
    print(val)

prompt()


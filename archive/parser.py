#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet TL : parser - requires Python version >= 3.10
"""

import sys
from math import factorial
assert sys.version_info >= (3, 10), "Use Python 3.10 or newer !"

import lexer
from definitions import V_T, str_attr_token

#####
# Variables internes (à ne pas utiliser directement)

_current_token = V_T.END
_value = None  # attribut du token renvoyé par le lexer

#####
# Fonctions génériques

class ParserError(Exception):
    pass

def unexpected_token(expected):
    return ParserError("Found token '" + _current_token.name + "' but expected " + expected)

def get_current():
    return _current_token

def init_parser(stream):
    global _current_token, _value
    lexer.reinit(stream)
    _current_token, _value = lexer.next_token()
    print("@ init parser on",  repr(str_attr_token(_current_token, _value)))  # for DEBUGGING

def consume_token(tok):
    # Vérifie que le prochain token est tok ;
    # si oui, le consomme et renvoie son attribut ; si non, lève une exception
    global _current_token, _value
    if _current_token != tok:
        raise unexpected_token(tok.name)
    if _current_token != V_T.END:
        old = _value
        _current_token, _value = lexer.next_token()
        return old

#########################
## Parsing de input et exp

def parse_exp():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:
        parse_exp_5()
        return 
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_0():
    if _current_token == V_T.NUM:
        consume_token(_current_token)
        return
    if _current_token == V_T.CALC:
        consume_token(_current_token)
        parse_exp_0()
        return
    if _current_token == V_T.OPAR:
        consume_token(_current_token)
        parse_exp_5()
        consume_token(V_T.CPAR)
        return 
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_1():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_exp_0()
        parse_exp_1_prime()
        return
    else:
        raise unexpected_token(_current_token.name)    

def parse_exp_1_prime():
    if _current_token == V_T.POW:
        consume_token(_current_token)
        parse_exp_1()
        return
    if _current_token in [V_T.END,V_T.ADD,V_T.SUB,V_T.CPAR, V_T.DIV,V_T.MUL,V_T.FACT,V_T.SEQ]:
        return
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_2():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_exp_1()
        parse_exp_2_prime()
        return 
    else:
        raise unexpected_token(_current_token.name)

def parse_exp_2_prime():
    if _current_token == V_T.FACT:
        consume_token(_current_token)
        parse_exp_2_prime()
    if _current_token in [V_T.END,V_T.ADD,V_T.SUB,V_T.CPAR, V_T.DIV,V_T.MUL,V_T.SEQ]:
        return
    else:
        raise unexpected_token(_current_token.name)
    _
def parse_exp_3():
    if _current_token== V_T.SUB:
        consume_token(_current_token)
        parse_exp_3()
        return
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR]:       
        parse_exp_2()
        return
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_4():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:
        parse_exp_3()
        parse_exp_4_prime()
        return
    else:
        raise unexpected_token(_current_token.name)

def parse_exp_4_prime():
    if _current_token == V_T.MUL:
        consume_token(_current_token)
        parse_exp_3()
        parse_exp_4_prime()
        return
    if _current_token == V_T.DIV:
        consume_token(_current_token)
        parse_exp_3()
        parse_exp_4_prime()
        return
    if _current_token in [V_T.END,V_T.ADD,V_T.SUB,V_T.CPAR,V_T.SEQ]:
        return
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_5():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:  
        parse_exp_4()
        parse_exp_5_prime()
        return
    else:
        raise unexpected_token(_current_token.name)
    
def parse_exp_5_prime():
    if _current_token==V_T.ADD:
        consume_token(_current_token)
        parse_exp_4()
        parse_exp_5_prime()
        return
    if _current_token==V_T.SUB:
        consume_token(_current_token)
        parse_exp_4()
        parse_exp_5_prime()
        return 
    if _current_token in [V_T.END,V_T.CPAR,V_T.SEQ]:
        return
    else:
        raise unexpected_token(_current_token.name)         

def parse_input():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB,V_T.END]:
        parse_input_prime()
        return
    else:
        raise unexpected_token(_current_token.name)
    
def parse_input_prime():
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:
        parse_exp()
        consume_token(V_T.SEQ)
        parse_input_prime()
        return
    if _current_token == V_T.END:
        return
    else:
        raise unexpected_token(_current_token.name)

"""
def parse_input():
    if _current_token == V_T.END:
        consume_token(_current_token)
        return
    if _current_token in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB,V_T.END]:
        
        parse_input()
        parse_exp()
        consume_token(V_T.SEQ)
        return
    else:
        raise unexpected_token(_current_token.name)
"""
#####################################
## Fonction principale de la calculatrice
## Appelle l'analyseur grammatical et retourne
## - None sans les attributs
## - la liste des valeurs des calculs avec les attributs

def parse(stream=sys.stdin):
    init_parser(stream)
    l = parse_input()
    consume_token(V_T.END)
    return l

#####################################
## Test depuis la ligne de commande

if __name__ == "__main__":
    print("@ Testing the calculator in infix syntax.")
    result = parse()
    if result is None:
        print("@ Input OK ")
    else:
        print("@ result = ", repr(result))

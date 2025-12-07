#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet TL : calc - requires Python version >= 3.10
"""

import sys
from math import factorial
assert sys.version_info >= (3, 10), "Use Python 3.10 or newer !"
import math
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
    return ParserError("Found token '" +str_attr_token( _current_token,_value) + "' but expected " + expected)

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

def parse_exp_0(l): # exp_0 -> NUM | CALC | OPAR exp_5 CPAR
    if get_current() == V_T.NUM:
        n = consume_token(get_current())
        return n
    if get_current() == V_T.CALC:
        i = consume_token(get_current())
        return l[i-1]
    if get_current() == V_T.OPAR:
        consume_token(get_current())
        n = parse_exp_5(l)
        consume_token(V_T.CPAR)
        return n
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_1(l): # exp_1 -> exp_0 exp_1' ( Factorisation )
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        n_1 = parse_exp_0(l)
        n = parse_exp_1_prime(n_1,l)
        return n
    else:
        raise unexpected_token(get_current().name)    

def parse_exp_1_prime(n_1,l): # exp_1' -> POW exp_1 | epsilon 
    if get_current() == V_T.POW:
        consume_token(V_T.POW)
        n_2 = parse_exp_1(l)
        return math.pow(n_1,n_2)
    if get_current() in [V_T.ADD,V_T.SUB,V_T.CPAR, V_T.DIV,V_T.MUL,V_T.FACT,V_T.SEQ]:
        return n_1
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_2(l): # exp_2 -> exp_1 exp_2' (Élimination de la Récursion Gauche)
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        n_1=parse_exp_1(l)
        n =parse_exp_2_prime(n_1,l)
        return n
    else:
        raise unexpected_token(get_current().name)

def parse_exp_2_prime(n_1,l): # exp_2' -> FACT exp_2' | epsilon 
    if get_current() == V_T.FACT:
        consume_token(get_current())
        n = parse_exp_2_prime(math.factorial(int(n_1)),l)
        return n
    if get_current() in [V_T.ADD,V_T.SUB,V_T.CPAR, V_T.DIV,V_T.MUL,V_T.SEQ]:
        return n_1
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_3(l): # exp_3 -> SUB exp_3 | exp_2
    if get_current()== V_T.SUB:
        consume_token(get_current())
        n_0= parse_exp_3(l)
        return -n_0
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR]:       
        n = parse_exp_2(l)
        return n
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_4(l): # exp_4 -> exp_3 exp_4' (Élimination de la Récursion Gauche)
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:
        n_1 = parse_exp_3(l)
        n = parse_exp_4_prime(n_1,l)
        return n
    else:
        raise unexpected_token(get_current().name)

def parse_exp_4_prime(n_1,l): #exp_4' -> MUL exp_3 exp_4'| DIV exp_3 exp_4' | epsilon
    if get_current() == V_T.MUL:
        consume_token(get_current())
        n_2 = parse_exp_3(l)
        n = parse_exp_4_prime(n_2*n_1,l)
        return n
    if get_current() == V_T.DIV:
        consume_token(get_current())
        n_3 = parse_exp_3(l)
        n = parse_exp_4_prime(n_1/n_3,l)
        return n
    if get_current() in [V_T.ADD,V_T.SUB,V_T.CPAR,V_T.SEQ]:
        return n_1
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_5(l): # exp_5 -> exp_4 exp_5' (Élimination de la Récursion Gauche)
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:  
        n_1= parse_exp_4(l)
        n = parse_exp_5_prime(n_1,l)
        return n
    else:
        raise unexpected_token(get_current().name)
    
def parse_exp_5_prime(n_1,l): # exp_5' -> ADD exp_4 exp_5'| SUB exp_4 exp_5' | epsilon
    if get_current()==V_T.ADD:
        consume_token(get_current())
        n_2 =parse_exp_4(l)
        n = parse_exp_5_prime(n_1+n_2,l)
        return n
    if get_current()==V_T.SUB:
        consume_token(get_current())
        n_3 = parse_exp_4(l)
        n = parse_exp_5_prime(n_1-n_3,l)
        return n
    if get_current() in [V_T.CPAR,V_T.SEQ]:
        return n_1
    else:
        raise unexpected_token(get_current().name)         

def parse_input(): # input -> input' END (Élimination de la Récursion Gauche)
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB,V_T.END]:
        l_init = []
        l = parse_input_prime(l_init)
        # La consommation du token V_T.END se trouve dans la fonction parse
        return l
    else:
        raise unexpected_token(get_current().name)
    
def parse_input_prime(l): # input' -> exp_5 SEQ input' | epsilon 
    if get_current() in [V_T.NUM,V_T.CALC,V_T.OPAR,V_T.SUB]:
        n = parse_exp_5(l)
        consume_token(V_T.SEQ)
        l.append(n)
        l_0 = parse_input_prime(l)
        return l_0
    if get_current() == V_T.END:
        return l
    else:
        raise unexpected_token(get_current().name)

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

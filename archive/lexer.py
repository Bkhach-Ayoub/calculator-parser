#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet TL : lexer de la calculatrice
"""

import sys
sys.path.append("/home/elfarchi/TL/projet-TL/archive/") # matnssach tmodifier lpath
import enum
import definitions as defs


# Pour lever une erreur, utiliser: raise LexerError("message décrivant l'erreur dans le lexer")
class LexerError(Exception):
    pass


#################################
# Variables et fonctions internes (privées)

# Variables privées : les trois prochains caractères de l'entrée
current_char1 = ''
current_char2 = ''
current_char3 = ''

# Initialisation: on vérifie que EOI n'est pas dans V_C et on initialise les prochains caractères
def init_char():
    global current_char1, current_char2, current_char3
    # Vérification de cohérence: EOI n'est pas dans V_C ni dans SEP
    if defs.EOI in defs.V_C:
        raise LexerError('character ' + repr(defs.EOI) + ' in V_C')
    defs.SEP = {' ', '\n', '\t'} - set(defs.EOI)
    defs.V = set(tuple(defs.V_C) + (defs.EOI,) + tuple(defs.SEP))
    current_char1 = defs.INPUT_STREAM.read(1)
    #print("@", repr(current_char1))  # decomment this line may help debugging
    if current_char1 not in defs.V:
        raise LexerError('Character ' + repr(current_char1) + ' unsupported')
    if current_char1 == defs.EOI:
        current_char2 = defs.EOI
        current_char3 = defs.EOI
    else:
        current_char2 = defs.INPUT_STREAM.read(1)
     #   print("@", repr(current_char2))  # decomment this line may help debugging
        if current_char2 not in defs.V:
            raise LexerError('Character ' + repr(current_char2) + ' unsupported')
        if current_char2 == defs.EOI:
            current_char3 = defs.EOI
        else:
            current_char3 = defs.INPUT_STREAM.read(1)
     #       print("@", repr(current_char3))  # decomment this line may help debugging
            if current_char3 not in defs.V:
                raise LexerError('Character ' + repr(current_char3) + ' unsupported')

    return

# Accès aux caractères de prévision
def peek_char3():
    global current_char1, current_char2, current_char3
    return (current_char1 + current_char2 + current_char3)

def peek_char1():
    global current_char1
    return current_char1

# Avancée d'un caractère dans l'entrée
def consume_char():
    global current_char1, current_char2, current_char3
    if current_char2 == defs.EOI: # pour ne pas lire au delà du dernier caractère
        current_char1 = defs.EOI
        return
    if current_char3 == defs.EOI: # pour ne pas lire au delà du dernier caractère
        current_char1 = current_char2
        current_char2 = defs.EOI
        return
    next_char = defs.INPUT_STREAM.read(1)
    #print("@", repr(next_char))  # decommenting this line may help debugging
    if next_char in defs.V:
        current_char1 = current_char2
        current_char2 = current_char3
        current_char3 = next_char
        return
    raise LexerError('Character ' + repr(next_char) + ' unsupported')

def expected_digit_error(char):
    return LexerError('Expected a digit, but found ' + repr(char))

def unknown_token_error(char):
    return LexerError('Unknown start of token ' + repr(char))

# Initialisation de l'entrée
def reinit(stream=sys.stdin):
    global input_stream, current_char1, current_char2, current_char3
    assert stream.readable()
    defs.INPUT_STREAM = stream
    current_char1 = ''
    current_char2 = ''
    current_char3 = ''
    init_char()


#################################
## Automates pour les entiers et les flottants

def step_INT_TO_EOI(state,ch):
    if state == 0 :
        if ch in defs.DIGITS:
            return 1
    elif state == 1:
        if ch in defs.DIGITS :
            return 1

def read_INT_to_EOI():
    state = 0
    ch = peek_char1()
    while ch != defs.EOI:
        state = step_INT_TO_EOI(state,ch)
        consume_char()
        ch = peek_char1()
    return state == 1

def step_FLOAT_TO_EOI(state,ch):
    if state == 0:
        if ch == ".":
            return 1
        elif ch in defs.DIGITS:
            return 2
    elif state == 1:
        if ch in defs.DIGITS:
            return 3
    elif state == 2:
        if ch in defs.DIGITS:
            return 2
        elif ch == '.':
            return 3
    elif state == 3:
        if ch in defs.DIGITS:
            return 3

def read_FLOAT_to_EOI():
    state = 0
    ch = peek_char1()
    while ch != defs.EOI:
        state = step_FLOAT_TO_EOI(state,ch)
        consume_char()
        ch = peek_char1()
    return state == 3


#################################
## Lecture de l'entrée: entiers, nombres, tokens


# Lecture d'un chiffre, puis avancée et renvoi de sa valeur
def read_digit():
    current_char = peek_char1()
    if current_char not in defs.DIGITS:
        raise expected_digit_error(current_char)
    value = eval(current_char)
    consume_char()
    return value


# Lecture d'un entier en renvoyant sa valeur
def read_INT():
    ch = peek_char1()
    if ch == defs.EOI or ch not in defs.DIGITS:
        return None
    rep = ''
    while defs.EOI not in ch:
        if ch not in defs.DIGITS:
            break
        else:
            rep = rep+ch
        consume_char()
        ch = peek_char1()
    print(rep)
    return rep

global int_value
global exp_value
global sign_value

# Lecture d'un nombre en renvoyant sa valeur

def transformation():
    return None

def read_NUM():
    int_value = ''
    exp_value = ''
    sign_value = ''
    Présence_de_point = False
    Présence_de_exp = False
    ch = peek_char1()
    S = 0
    while defs.EOI not in ch:
        if ch == '.':
            Présence_de_point = True
        elif ch in defs.DIGITS:
            if Présence_de_exp:
                exp_value = exp_value+ch
            else: 
                int_value = int_value+ ch
            if Présence_de_point:
                S+=1
        elif ch =='e'or ch == 'E':
            Présence_de_exp = True
            Présence_de_point = False
        elif ch == '+' or ch =='-':
            sign_value += ch
        consume_char()
        ch = peek_char1()
    if Présence_de_point:
        if exp_value == '':
            exp_value = str(S)
        if sign_value == '':
            sign_value ='-'
    if exp_value =='':
        exp_value ='0'
    if S != 0 and Présence_de_exp:
        if exp_value == '0':
            sign_value = '-'
            exp_value = str(int(exp_value)+S)
        else :
            if sign_value == '-':
                exp_value = str(int(exp_value)+S)
            else :
                exp_value = str(int(exp_value)-S)
        return int_value+"e"+sign_value+exp_value
    return int_value+"e"+sign_value+exp_value


# Parse un lexème (sans séparateurs) de l'entrée et renvoie son token.
# Cela consomme tous les caractères du lexème lu.
def read_token_after_separators():
    print("@ATTENTION: lexer.read_token_after_separators à finir !") # LIGNE A SUPPRIMER
    return (defs.V_T.END, None) # par défaut, on renvoie la fin de l'entrée


# Donne le prochain token de l'entrée, en sautant les séparateurs éventuels en tête
# et en consommant les caractères du lexème reconnu.
def next_token():
    print("@ATTENTION: lexer.next_token à finir !") # LIGNE A SUPPRIMER
    return read_token_after_separators()


#################################
## Fonctions de tests

def test_INT_to_EOI():
    print("@ Testing read_INT_to_EOI. Type a word to recognize.")
    reinit()
    if read_INT_to_EOI():
        print("Recognized")
    else:
        print("Not recognized")

def test_FLOAT_to_EOI():
    print("@ Testing read_FLOAT_to_EOI. Type a word to recognize.")
    reinit()
    if read_FLOAT_to_EOI():
        print("Recognized")
    else:
        print("Not recognized")

def test_lexer():
    print("@ Testing the lexer. Just type tokens and separators on one line")
    reinit()
    token, value = next_token()
    while token != defs.V_T.END:
        print("@", defs.str_attr_token(token, value))
        token, value = next_token()

if __name__ == "__main__":
    ## Choisir une seule ligne à décommenter
    # test_INT_to_EOI()
    # test_FLOAT_to_EOI()
    test_lexer()

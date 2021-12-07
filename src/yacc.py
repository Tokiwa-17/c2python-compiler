# -*- coding=utf-8 -*-

from lex import tokens
from ast import *
import ply.yacc as yacc


 def p_empty(p):
     'empty :'
     pass

def p_error(p):
    print('[YACC Error] type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))

# 6.8
def p_statement(p):
    ''' statement : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement'''
    p[0] = ASTInternalNode('statement', p[1:])

# 6.8.1
def p_labeled_statement(p):
    ''' labeled_statement : identifier ':' statement
                          | CASE constant_expression ':' statement
                          | DEFAULT ':' statement '''
    p[0] = ASTInternalNode('labeled_statement', p[1:])

# 6.8.2
def p_compound_statement(p):
    ''' compound_statement : '{' '}'
                           | '{' block_item_list '}' '''
    p[0] = ASTInternalNode('compound_statement', p[1:])

# 6.8.2
def p_block_item_list(p):
    ''' block_item_list : block_item
                        | block_item_list block_item '''
    p[0] = ASTInternalNode('block_item_list', p[1:])

# 6.8.2
def p_block_item(p):
    ''' block_item : declaration
                   | statement '''
    p[0] = ASTInternalNode('block_item', p[1:])

# 6.8.3
def p_expression_statement(p):
    ''' expression_statement : empty
                             | expression '''
    p[0] = ASTInternalNode('expression_statement')

# 6.8.4
def p_selection_statement(p):
    ''' selection_statement : IF '(' expression ')' statement
                            | IF '(' expression ')' ELSE statement
                            | SWITCH '(' expression ')' statement '''
    p[0] = ASTInternalNode('selection_statement')

# 6.8.5
def p_iteration_statement(p):
    ''' iteration_statement : WHILE '(' expression ')' statement
                            | DO statement WHILE '(' expression ')' ';'
                            | FOR '(' ';' ';' ')' statement
                            | FOR '(' expression ';' ';' ')' statement
                            | FOR '(' ';' expression ';' ')' statement
                            | FOR '(' ';' ';' expression ')' statement
                            | FOR '(' expression ';' expression ';' ')' statement
                            | FOR '(' ';' expression ';' expression ')' statement
                            | FOR '(' expression ';' ';' expression ')' statement
                            | FOR '(' expression ';' expression ';' expression ')' statement
                            | FOR '(' declaration ';' ')' statement
                            | FOR '(' declaration ';' expression ')' statement
                            | FOR '(' declaration expression ';' ')' statement
                            | FOR '(' declaration expression ';' expression ')' statement '''
    p[0] = ASTInternalNode('iteration_statement')

# 6.8.6
def p_jump_statement(p):
    ''' jump_statement : GOTO identifier ';'
                       | CONTINUE ';'
                       | BREAK ';'
                       | RETURN ';'
                       | RETURN expression ';' '''
    p[0] = ASTInternalNode('jump_statement')

# 6.9
def p_translation_unit(p):
    ''' translation_unit : external_declaration
                         | translation_unit external_declaration '''
    p[0] = ASTInternalNode('translation_unit', p[1:])

# 6.9
def p_external_declaration(p):
    ''' external_declaration : function_definition
                             | declaration '''
    p[0] = ASTInternalNode('external_declaration', p[1:])

# 6.9.1
def p_function_definition(p):
    ''' function_definition : declaration_specifiers declarator declaration_list compound_statement
                            | declaration_specifiers declarator compound_statement '''
    p[0] = ASTInternalNode('function_definition', p[1:])

# 6.9.1
def p_declaration_list(p):
    ''' declaration_list : declaration
                         | declaration_list declaration '''
    p[0] = ASTInternalNode('declaration_list', p[1:])

parser = yacc.yacc()

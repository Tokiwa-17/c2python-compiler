# -*- coding=utf-8 -*-

from lex import tokens
from ast import *
import ply.yacc as yacc
from lex import tokens


# 入口
def p_translation_unit(p):
    ''' translation_unit : external_declaration
                         | translation_unit external_declaration '''
    p[0] = ASTInternalNode('translation_unit', p[1:])


def p_external_declaration(p):
    ''' external_declaration : function_definition
                             | declaration '''
    p[0] = ASTInternalNode('external_declaration', p[1:])

# 6.5.1
def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                          | CONSTANT
                          | STRING_LITERAL
                          | '(' expression ')' '''
    p[0] = ASTInternalNode('primary_expression', p[1:])


# 6.5.2
# TODO: 此处第6行产生式的PTR_OP在原文档中为'->'，而在lex.py中被写为' -> / ->'
def p_postfix_expression(p):
    ''' postfix_expression : primary_expression
                           | postfix-expression '[' expression ']'
                           | postfix-expression '(' ')'
                           | postfix-expression '(' argument-expression-listopt ')'
                           | postfix-expression '.' IDENTIFIER
                           | postfix-expression PTR_OP IDENTIFIER
                           | postfix-expression INC_DEC
                           | '(' type_name ')' '{' initializer_list '}'
                           | '(' type_name ')' '{' initializer_list ',' '}' '''
    p[0] = ASTInternalNode('postfix_expression', p[1:])


# 6.5.2(2)
def p_argument_expression_list(p):
    ''' argument_expression_list : assignment_expression
                                 | argument-expression-list ',' assignment-expression '''
    p[0] = ASTInternalNode('argument_expression_list', p[1:])


# 6.5.3
def p_unary_expression(p):
    ''' unary_expression : postfix_expression
                         | INC_DEC unary_expression
                         | unary_operator cast_expression
                         | SIZEOF unary_expression
                         | SIZEOF '(' type_name ')' '''
    p[0] = ASTInternalNode('unary_expression', p[1:])


# 6.5.3(2)
def p_unary_operator(p):
    ''' unary_operator : '&'
                       | '*'
                       | '+'
                       | '-'
                       | '~'
                       | '!' '''
    p[0] = ASTInternalNode('unary_operator', p[1:])


# 6.5.4
def p_cast_expression(p):
    ''' cast_expression : unary_expression
                        | '(' type_name ')' cast_expression '''
    p[0] = ASTInternalNode('cast_expression', p[1:])


# 6.5.5
def p_multiplicative_expression(p):
    ''' multiplicative_expression : cast_expression
                                  | multiplicative_expression '*' cast_expression
                                  | multiplicative_expression '/' cast_expression
                                  | multiplicative_expression '%' cast_expression '''
    p[0] = ASTInternalNode('multiplicative_expression', p[1:])


# 6.5.6
def p_additive_expression(p):
    ''' additive_expression : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative-expression '''
    p[0] = ASTInternalNode('additive_expression', p[1:])


# 6.5.7
def p_shift_expression(p):
    ''' shift-expression : additive_expression
                         | shift_expression SHIFT_OP additive_expression '''
    p[0] = ASTInternalNode('shift_expression', p[1:])


# 6.5.8
def p_relational_expression(p):
    ''' relational_expression : shift_expression
                              | relational_expression '<' shift_expression
                              | relational_expression '>' shift_expression
                              | relational_expression GE_LE shift_expression '''
    p[0] = ASTInternalNode('relational_expression', p[1:])


# 6.5.9
def p_equality_expression(p):
    ''' equality_expression : relational_expression
                            | equality_expression EQ_NE relational_expression '''
    p[0] = ASTInternalNode('equality_expression', p[1:])


# 6.5.10
def p_and_expression(p):
    ''' and_expression : equality_expression
                       | and_expression '&' equality_expression '''
    p[0] = ASTInternalNode('and_expression', p[1:])


# 6.5.11
def p_exclusive_or_expression(p):
    ''' exclusive_or_expression : and_expression
                                | exclusive_or_expression '^' and_expression '''
    p[0] = ASTInternalNode('exclusive_or_expression', p[1:])


# 6.5.12
def p_inclusive_or_expression(p):
    ''' inclusive_or_expression : exclusive_or_expression
                                | inclusive_or_expression '|' exclusive_or_expression '''
    p[0] = ASTInternalNode('inclusive_or_expression', p[1:])


# 6.5.13
def p_logical_and_expression(p):
    ''' logical_and_expression : inclusive_or_expression
                               | logical_and_expression AND_OP inclusive_or_expression '''
    p[0] = ASTInternalNode('logical_and_expression', p[1:])


# 6.5.14
def p_logical_or_expression(p):
    ''' logical_or_expression : logical_and_expression
                              | logical_or_expression OR_OP logical_and_expression '''
    p[0] = ASTInternalNode('logical_or_expression', p[1:])


# 6.5.15
def p_conditional_expression(p):
    ''' conditional_expression : logical_or_expression
                               | logical_or_expression '?' expression ':' conditional_expression '''
    p[0] = ASTInternalNode('conditional_expression', p[1:])


# 6.5.16
def p_assignment_expression(p):
    ''' assignment_expression : conditional_expression
                              | unary_expression assignment_operator assignment_expression '''
    p[0] = ASTInternalNode('assignment_expression', p[1:])


#6.5.16(2)
def p_assignment_operator(p):
    ''' assignment_operator : ASSIGN_OP '''
    p[0] = ASTInternalNode('assignment_operator', p[1:])


# 6.5.17
def expression(p):
    ''' expression : assignment_expression
                   | expression ',' assignment_expression '''
    p[0] = ASTInternalNode('expression', p[1:])



def p_error(p):
    print('[YACC Error] type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))


parser = yacc.yacc()

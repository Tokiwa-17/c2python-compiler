# -*- coding=utf-8 -*-

from lex import tokens
from ast import *
import ply.yacc as yacc


# 入口
def p_translation_unit(p):
    ''' translation_unit : external_declaration
                         | translation_unit external_declaration '''
    p[0] = ASTInternalNode('translation_unit', p[1:])


def p_external_declaration(p):
    ''' external_declaration : function_definition
                             | declaration '''
    p[0] = ASTInternalNode('external_declaration', p[1:])


def p_error(p):
    print('[YACC Error] type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))

# 6.7.5
def p_declarator(p):
    ''' declarator : pointer direct_declarator
                   | direct_declarator '''
    p[0] = ASTInternalNode('declaration', p[1:])

# 6.7.5
def p_direct_declarator(p):
    ''' direct_declarator : IDENTIFIER
                          | '(' declarator ')'
                          | direct_declarator '[' type_qualifier_list assignment_expression ']'
                          | direct_declarator '[' assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list ']'
                          | direct_declarator '[' ']'
                          | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                          | direct_declarator '[' STATIC assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list '*' ']'
                          | direct_declarator '[' '*' ']'
                          | direct_declarator '(' parameter_type_list ')' 
                          | direct_declarator '(' identifier_list ')'
                          | direct_declarator '(' ')' '''
    p[0] = ASTInternalNode('direct_declarator', p[1:])

# 6.7.5
def p_pointer(p):
    ''' pointer : '*' type_qualifier_list
                | '*'
                | '*' type_qualifier_list pointer
                | '*' pointer '''
    p[0] = ASTInternalNode('pointer', p[1:])

# 6.7.5
def p_type_qualifier_list(p):
    ''' type_qualifier_list : type_qualifier
                            | type_qualifier_list type_qualifier '''
    p[0] = ASTInternalNode('type_qualifier_list', p[1:])

# 6.7.5
def p_parameter_type_list(p):
    ''' parameter_type_list : parameter_list
                            | parameter_list ',' ELLIPSIS '''
    p[0] = ASTInternalNode('parameter_type_list', p[1:])

# 6.7.5
def p_parameter_list(p):
    ''' parameter_list : parameter_declaration
                       | parameter_list ',' parameter_declaration '''
    p[0] = ASTInternalNode('parameter_list', p[1:])

# 6.7.5
def p_parameter_declaration(p):
    ''' parameter_declaration : declaration_specifiers declarator
                              | declaration_specifiers abstract_declarator
                              | declaration_specifiers '''
    p[0] = ASTInternalNode('parameter_declaration', p[1:])

# 6.7.5
def p_identifier_list(p):
    ''' identifier_list : IDENTIFIER
                        | identifier_list ',' IDENTIFIER '''
    p[0] = ASTInternalNode('identifier_list', p[1:])

# 6.7.6
def p_type_name(p):
    ''' type_name : specifier_qualifier_list
                  | specifier_qualifier_list abstract_declarator '''
    p[0] = ASTInternalNode('type_name', p[1:])

# 6.7.6
def p_abstract_declarator(p):
    ''' abstract_declarator : pointer
                            | direct_abstract_declarator
                            | pointer direct_abstract_declarator '''
    p[0] = ASTInternalNode('abstract_declarator', p[1:])

# 6.7.6
def p_direct_abstract_declarator(p):
    ''' direct_abstract_declarator : '(' abstract_declarator ')'
                                   | '[' ']'
                                   | '[' assignment_expression ']'
                                   | direct_abstract_declarator '[' ']'
                                   | direct_abstract_declarator '[' assignment_expression ']'
                                   | '[' type_qualifier_list ']'
                                   | '[' type_qualifier_list assignment_expression ']'
                                   | direct_abstract_declarator '[' type_qualifier_list ']'
                                   | direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'
                                   | direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                                   | '[' STATIC type_qualifier_list assignment_expression ']'
                                   | direct_abstract_declarator '[' STATIC assignment_expression ']'
                                   | '[' STATIC assignment_expression ']'
                                   | direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                                   | '[' type_qualifier_list STATIC assignment_expression ']'
                                   | '[' '*' ']'
                                   | direct_abstract_declarator '[' '*' ']'
                                   | '(' ')'
                                   | '(' parameter_type_list ')'
                                   | direct_abstract_declarator '(' ')'
                                   | direct_abstract_declarator '(' parameter_type_list ')' '''
    p[0] = ASTInternalNode('direct_abstract_declarator', p[1:])

# 6.7.7
def p_typedef_name(p):
    ''' typedef_name: IDENTIFIER'''
    p[0] = ASTInternalNode('typedef_name', p[1:])

# 6.7.8
def p_initializer(p):
    ''' initializer : assignment_expression
                    | '{' initializer_list '}'
                    | '{' initializer_list ',' '}' '''
    p[0] = ASTInternalNode('initializer', p[1:])

# 6.7.8
def p_initializer_list(p):
    ''' initializer_list : initializer
                         | designation initializer
                         | initializer_list ',' initializer
                         | initializer_list ',' designation initializer '''
    p[0] = ASTInternalNode('initializer_list', p[1:])

# 6.7.8
def p_designation(p):
    ''' designation : designator_list '=' '''
    p[0] = ASTInternalNode('designation', p[1:])

# 6.7.8
def p_designator_list(p):
    ''' designator_list : designator
                        | designator_list designator '''
    p[0] = ASTInternalNode('designator_list', p[1:])

# 6.7.8
def p_designator(p):
    ''' designator : '[' constant_expression ']'
                   | '.' IDENTIFIER '''
    p[0] = ASTInternalNode('designator', p[1:])
parser = yacc.yacc()

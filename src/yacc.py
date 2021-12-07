# -*- coding=utf-8 -*-

from lex import tokens
from ast import *
import ply.yacc as yacc


# 6.7
def p_declaration(p):
    ''' declaration : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';' '''
    p[0] = ASTInternalNode('declaration', p[1:])


# 6.7
def p_declaration_specifiers(p):
    ''' declaration_specifiers : storage_class_specifier
                               | storage_class_specifier declaration_specifiers
                               | type_specifier
                               | type_specifier declaration_specifiers
                               | type_qualifier 
                               | type_qualifier declaration_specifiers
                               | function_specifier
                               | function_specifier declaration_specifiers '''
    p[0] = ASTInternalNode('declaration_specifiers', p[1:])


# 6.7
def p_init_declarator_list(p):
    ''' init_declarator_list : init_declarator
                             | init_declarator_list ',' init_declarator '''
    p[0] = ASTInternalNode('init_declarator_list', p[1:])


# 6.7
def p_init_declarator(p):
    ''' init_declarator : declarator
                        | declarator '=' initializer'''
    p[0] = ASTInternalNode('init_declarator', p[1:])


# 6.7.1
def p_storage_class_specifier(p):
    ''' storage_class_specifier : TYPEDEF | EXTERN | STATIC | AUTO | REGISTER '''
    p[0] = ASTInternalNode('storage_class_specifier', p[1:])


# 6.7.2
def p_type_specifier(p):
    ''' type_specifier : VOID | CHAR | SHORT | INT | LONG | FLOAT | DOUBLE | SIGNED | UNSIGNED | BOOL
                       | struct_or_union_specifier
                       | enum_specifier
                       | typedef_name '''
    p[0] = ASTInternalNode('type_specifier', p[1:])


# 6.7.2.1
def p_struct_or_union_specifier(p):
    ''' struct_or_union_specifier : struct_or_union '{' struct_declaration_list '}'
                                  | struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                  | struct_or_union IDENTIFIER '''
    p[0] = ASTInternalNode('struct_or_union_specifier', p[1:])


# 6.7.2.1
def p_struct_or_union(p):
    ''' struct_or_union : STRUCT | UNION '''
    p[0] = ASTInternalNode('struct_or_union', p[1:])


# 6.7.2.1
def p_struct_declaration_list(p):
    ''' struct_declaration_list : struct_declaration
                                | struct_declaration_list struct_declaration '''
    p[0] = ASTInternalNode('struct_declaration_list', p[1:])


# 6.7.2.1
def p_struct_declaration(p):
    ''' struct_declaration : specifier_qualifier_list struct_declarator_list ';' '''
    p[0] = ASTInternalNode('struct_declaration', p[1:])


# 6.7.2.1
def p_specifier_qualifier_list(p):
    ''' specifier_qualifier_list : type_specifier
                                 | type_specifier specifier_qualifier_list
                                 | type_qualifeir
                                 | type_qualifeir specifier_qualifier_list '''
    p[0] = ASTInternalNode('specifier_qualifier_list', p[1:])


# 6.7.2.1
def p_struct_declarator_list(p):
    ''' struct_declarator_list : struct_declarator
                               | struct_declarator_list struct_declarator '''
    p[0] = ASTInternalNode('struct_declarator_list', p[1:])


# 6.7.2.1
def p_struct_declarator(p):
    ''' struct_declarator : declarator
                          | ':' constant_expression
                          | declarator ':' constant_expression'''
    p[0] = ASTInternalNode('struct_declarator', p[1:])


# 6.7.2.2
def p_enum_specifier(p):
    ''' enum_specifier : ENUM '{' enumerator_list '}'
                       | ENUM IDENTIFIER '{' enumerator_list '}'
                       | ENUM '{' enumerator_list ',' '}'
                       | ENUM IDENTIFIER '{' enumerator_list, '}'
                       | ENUM IDENTIFIER '''
    p[0] = ASTInternalNode('enum_specifier', p[1:])


# 6.7.2.2
def p_enumerator_list(p):
    ''' enumerator_list : enumerator
                        | enumerator_list enumerator '''
    p[0] = ASTInternalNode('enumerator_list', p[1:])


# 6.7.2.2
def p_enumerator(p):
    ''' enumerator : enumeration_constant
                   | enumeration_constant '=' constant_expression '''
    p[0] = ASTInternalNode('enumerator', p[1:])


# 6.7.3
def p_type_qualifier(p):
    ''' type_qualifier : CONST | RESTRICT | VOLATILE '''
    p[0] = ASTInternalNode('type_qualifier', p[1:])


# 6.7.4
def p_function_specifier(p):
    ''' function_specifier : INLINE '''
    p[0] = ASTInternalNode('function_specifier', p[1:])


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


parser = yacc.yacc()

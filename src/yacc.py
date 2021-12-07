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


parser = yacc.yacc()

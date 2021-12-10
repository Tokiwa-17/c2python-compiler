# -*- coding=utf-8 -*-

import ply.lex as lex
from ply.lex import TOKEN

reserved = {
    'auto': 'AUTO',
    'break': 'BREAK',
    'bool': 'BOOL',
    'case': 'CASE',
    'char': 'CHAR',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do': 'DO',
    'double': 'DOUBLE',
    'else': 'ELSE',
    'enum': 'ENUM',
    'extern': 'EXTERN',
    'float': 'FLOAT',
    'for': 'FOR',
    'goto': 'GOTO',
    'if': 'IF',
    'inline': 'INLINE',
    'int': 'INT',
    'long': 'LONG',
    'register': 'REGISTER',
    'restrict': 'RESTRICT',
    'return': 'RETURN',
    'short': 'SHORT',
    'signed': 'SIGNED',
    'sizeof': 'SIZEOF',
    'static': 'STATIC',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'typedef': 'TYPEDEF',
    'union': 'UNION',
    'unsigned': 'UNSIGNED',
    'void': 'VOID',
    'volatile': 'VOLATILE',
    'while': 'WHILE',
}

tokens = (
    'IDENTIFIER',
    'CONSTANT',
    'STRING_LITERAL',
    'ELLIPSIS',  # ...
    'PTR_OP',  # ->, ->*
    'INC_DEC',  # ++, --
    'SHIFT_OP',  # <<, >>
    'GE_LE',  # >=, <=
    'EQ_NE',  # ==, !=
    'AND_OP',
    'OR_OP',
    'ASSIGN_OP',  # += , <<=, etc. (not include =)
)

tokens = tokens + tuple(reserved.values())

# 数字 - 十进制
D = r'[0-9]'
# 数字 - 十六进制
H = r'[0-9a-fA-F]'
# 下划线与字母
L = r'([_a-zA-Z])'
# 科学计数法后缀
E = r'[Ee][+-]?[0-9]+'
# 浮点数修饰符
FS = r'(f|F|l|L)'
# 整型数修饰符
IS = r'(u|U|l|L)*'


@TOKEN(r'(%s(%s|%s)*)' % (L, D, L))
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


boolean = r'(true|false)'
integer = r'(0?%s+%s?|0[xX]%s+%s?|%s+%s%s?)' % (D, IS, H, IS, D, E, FS)
decimal = r'((%s+\.%s*(%s)?%s?)|(%s*\.%s+(%s)?%s?))' % (D,
                                                        D, E, FS, D, D, E, FS)
char = r'(\'(\\.|[^\\\'])+\')'
identifier = r'(%s(%s|%s)*)' % (L, D, L)

t_CONSTANT = r'(%s|%s|%s|%s)' % (decimal, integer, char, boolean)
t_STRING_LITERAL = r'"(\\.|[^\\"])*"'
t_ELLIPSIS = r'\.\.\.'
t_PTR_OP = r'(->|->\*)'
t_INC_DEC = r'(\+\+|--)'
t_SHIFT_OP = r'(<<|>>)'
t_GE_LE = r'(>=|<=)'
t_EQ_NE = r'(==|!=)'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_ASSIGN_OP = r'(\*=|/=|%=|\+=|-=|&=|\|=|^=|<<=|>>=)'


literals = '#;,.?:[](){}<=>+-*/%&|!~^'
t_ignore = ' \t\v\f'


def t_COMMENT(t):
    r'//[^\n]*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("[Lex Error] Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def find_column(string, token):
    '''
    Compute column
    
    Parameters
    --------
    + `string` - the input text string
    + `token` - a lex token instance
    '''
    last_cr = string.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# 构建词法分析器
lexer = lex.lex()


# 测试程序
if __name__ == '__main__':
    while True:
        try:
            filepath = input('lex > ')
            with open(filepath, 'r') as file:
                data = file.read()
                lex.input(data)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, find_column(data, tok))
        except EOFError:
            break

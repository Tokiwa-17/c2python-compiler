import ply.lex as lex
from ply.lex import TOKEN

tokens = (
    'ASSIGN',
)


reserved = {
    'auto': 'AUTO',
    'break': 'BREAK',
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
    'int': 'INT',
    'long': 'LONG',
    'register': 'REGISTER',
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
    'while': 'WHILE'
}
tokens = tokens + tuple(reserved.values())

t_ASSIGN = r'=|\+=|-=|\*=|/=|%=|<<=|>>=|&=|\^=|\|='

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\v\f'

def t_COMMENT(t):
    r'//[^\n]*'
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Compute column.
#     string is the input text string
#     token is a token instance
def find_column(string, token):
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
                print(data)
                lex.input(data)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, find_column(data, tok))
        except EOFError:
            break
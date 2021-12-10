# coding=utf-8
import re
import ply.yacc as yacc
from lex import tokens, identifier
from ast_ import *

def p_translation_unit(p):
    ''' translation_unit : external_declaration
                         | translation_unit external_declaration '''
    p[0] = ASTInternalNode('translation_unit', p[1:])

# 6.5.1
def p_primary_expression(p):
    ''' primary_expression : IDENTIFIER
                           | CONSTANT
                           | STRING_LITERAL
                           | '(' expression ')' '''
    p[0] = ASTInternalNode('primary_expression', p[1:])

# 6.5.2
def p_postfix_expression(p):
    ''' postfix_expression : primary_expression
                           | postfix_expression '[' expression ']'
                           | postfix_expression '(' ')'
                           | postfix_expression '(' argument_expression_list ')'
                           | postfix_expression '.' IDENTIFIER
                           | postfix_expression PTR_OP IDENTIFIER
                           | postfix_expression INC_DEC
                           | '(' type_name ')' '{' initializer_list '}'
                           | '(' type_name ')' '{' initializer_list ',' '}' '''
    p[0] = ASTInternalNode('postfix_expression', p[1:])

# 6.5.2
def p_argument_expression_list(p):
    ''' argument_expression_list : assignment_expression
                                 | argument_expression_list ',' assignment_expression '''
    p[0] = ASTInternalNode('argument_expression_list', p[1:])

# 6.5.3
def p_unary_expression(p):
    ''' unary_expression : postfix_expression
                         | INC_DEC unary_expression
                         | unary_operator cast_expression
                         | SIZEOF unary_expression
                         | SIZEOF '(' type_name ')' '''
    p[0] = ASTInternalNode('unary_expression', p[1:])

# 6.5.3
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
                            | additive_expression '-' multiplicative_expression '''
    p[0] = ASTInternalNode('additive_expression', p[1:])

# 6.5.7
def p_shift_expression(p):
    ''' shift_expression : additive_expression
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
def p_constant_expression(p):
    ''' constant_expression : conditional_expression '''
    p[0] = ASTInternalNode('constant_expression', p[1:])

# 6.5.17
def p_assignment_operator(p):
    ''' assignment_operator : '='
                            | ASSIGN_OP '''
    p[0] = ASTInternalNode('assignment_operator', p[1:])

# 6.6

# 6.7
def p_declaration(p):
    ''' declaration : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';' '''
    p[0] = ASTInternalNode('declaration', p[1:])

# 6.7
def p_declaration_specifiers(p):
    ''' declaration_specifiers 	: storage_class_specifier
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
                        | declarator '=' initializer '''
    p[0] = ASTInternalNode('init_declarator', p[1:])

# 6.7.1
def p_storage_class_specifier(p):
    ''' storage_class_specifier : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER '''
    p[0] = ASTInternalNode('storage_class_specifier', p[1:])

# 6.7.2
def p_type_specifier(p):
    ''' type_specifier : VOID
                       | CHAR
                       | SHORT
                       | INT
                       | LONG
                       | FLOAT
                       | DOUBLE
                       | SIGNED
                       | UNSIGNED
                       | BOOL
                       | struct_or_union_specifier
                       | enum_specifier '''
    p[0] = ASTInternalNode('type_specifier', p[1:])

# 6.7.2.1
def p_struct_or_union_specifier(p):
    ''' struct_or_union_specifier : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                  | struct_or_union '{' struct_declaration_list '}'
                                  | struct_or_union IDENTIFIER '''
    if not p[2] == '{' and not p[2] in reserved_list:
        p[2] = ASTExternalNode('IDENTIFIER', p[2])
    p[0] = ASTInternalNode('struct_or_union_specifier', p[1:])

# 6.7.2.1
def p_struct_or_union(p):
    ''' struct_or_union : STRUCT
                        | UNION '''
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
    ''' specifier_qualifier_list : type_specifier specifier_qualifier_list
                                 | type_specifier
                                 | type_qualifier specifier_qualifier_list
                                 | type_qualifier  '''
    p[0] = ASTInternalNode('specifier_qualifier_list', p[1:])

# 6.7.2.1
def p_struct_declarator_list(p):
    ''' struct_declarator_list : struct_declarator
                               | struct_declarator_list ',' struct_declarator '''
    p[0] = ASTInternalNode('struct_declarator_list', p[1:])

# 6.7.2.1
def p_struct_declarator(p):
    ''' struct_declarator : declarator
                          | ':' constant_expression
                          | declarator ':' constant_expression '''
    p[0] = ASTInternalNode('struct_declarator', p[1:])

# 6.7.2.2
def p_enum_specifier(p):
    ''' enum_specifier : ENUM '{' enumerator_list '}'
                        | ENUM IDENTIFIER '{' enumerator_list '}'
                        | ENUM '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER '''
    p[0] = ASTInternalNode('enum_specifier', p[1:])

# 6.7.2.2
def p_enumerator_list(p):
    ''' enumerator_list : enumerator
                        | enumerator_list ',' enumerator '''
    p[0] = ASTInternalNode('enumerator_list', p[1:])

# 6.7.2.2
def p_enumerator(p):
    ''' enumerator : IDENTIFIER
                   | IDENTIFIER '=' constant_expression '''
    p[0] = ASTInternalNode('enumerator', p[1:])

# 6.7.3
def p_type_qualifier(p):
    ''' type_qualifier : CONST
                       | RESTRICT
                       | VOLATILE '''
    p[0] = ASTInternalNode('type_qualifier', p[1:])

# 6.7.4
def p_function_specifier(p):
    ''' function_specifier : INLINE '''
    p[0] = ASTInternalNode('function_specifier', p[1:])

# 6.7.5
def p_declarator(p):
    ''' declarator : pointer direct_declarator
                   | direct_declarator '''
    p[0] = ASTInternalNode('declarator', p[1:])

# 6.7.5
def p_direct_declarator(p):
    ''' direct_declarator : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list ']'
                        | direct_declarator '[' assignment_expression ']'
                        | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list '*' ']'
                        | direct_declarator '[' '*' ']'
                        | direct_declarator '[' ']'
                        | direct_declarator '(' parameter_type_list ')'
                        | direct_declarator '(' identifier_list ')'
                        | direct_declarator '(' ')' '''
    p[0] = ASTInternalNode('direct_declarator', p[1:])

# 6.7.5
def p_pointer(p):
    ''' pointer : '*'
                | '*' type_qualifier_list
                | '*' pointer
                | '*' type_qualifier_list pointer '''
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
                                   | '[' '*' ']'
                                   | direct_abstract_declarator '[' '*' ']'
                                   | '(' ')'
                                   | '(' parameter_type_list ')'
                                   | direct_abstract_declarator '(' ')'
                                   | direct_abstract_declarator '(' parameter_type_list ')' '''
    p[0] = ASTInternalNode('direct_abstract_declarator', p[1:])

# 6.7.7

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

# 6.8
def p_statement(p):
    ''' statement : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement '''
    p[0] = ASTInternalNode('statement', p[1:])

# 6.8.1
def p_labeled_statement(p):
    ''' labeled_statement : IDENTIFIER ':' statement
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
    ''' expression_statement : ';'
                             | expression ';' '''
    p[0] = ASTInternalNode('expression_statement', p[1:])

# 6.8.4
def p_selection_statement(p):
    ''' selection_statement : IF '(' expression ')' statement ELSE statement
                            | IF '(' expression ')' statement
                            | SWITCH '(' expression ')' statement '''
    p[0] = ASTInternalNode('selection_statement', p[1:])

# 6.8.5
def p_iteration_statement(p):
    ''' iteration_statement : WHILE '(' expression ')' statement
                            | DO statement WHILE '(' expression ')' ';'
                            | FOR '(' expression_statement expression_statement ')' statement
                            | FOR '(' expression_statement expression_statement expression ')' statement
                            | FOR '(' declaration expression_statement ')' statement
                            | FOR '(' declaration expression_statement expression ')' statement '''
    p[0] = ASTInternalNode('iteration_statement', p[1:])

# 6.8.6
def p_jump_statement(p):
    ''' jump_statement : GOTO IDENTIFIER ';'
                       | CONTINUE ';'
                       | BREAK ';'
                       | RETURN ';'
                       | RETURN expression ';' '''
    p[0] = ASTInternalNode('jump_statement', p[1:])

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


def p_expression(p):
    ''' expression : assignment_expression
                   | expression ',' assignment_expression '''
    p[0] = ASTInternalNode('expression', p[1:])

def p_assignment_expression(p):
    ''' assignment_expression : conditional_expression
                              | unary_expression assignment_operator assignment_expression '''
    p[0] = ASTInternalNode('assignment_expression', p[1:])

def p_error(p):
    print('[Error]: type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))
parser = yacc.yacc()

# 测试程序
if __name__ == '__main__':
    while True:
        try:
            s = input('yacc > ')
            with open(s, 'r') as file:
                result = parser.parse(file.read())
                print(result)
        except EOFError:
            break
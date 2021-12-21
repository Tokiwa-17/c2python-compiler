from preprocessing import precompile
from yacc import parser
#from c_utils import c_utils
from ast_ import ASTLeafNode, ASTInternalNode
import copy

class Interpreter:
    def __init__(self, src_file, dst_file):
        self.src_file = src_file
        self.dst_file = dst_file
        self.import_cmd = None
        #print(src_file)
        if self.src_file.split('.')[-1] != 'c':
            raise Exception('The type of source file is incorrect.')
        if self.dst_file.split('.')[-1] != 'py':
            raise Exception('The type of destin`ation file is incorrect.')

        self.global_variables = []
        self.functions = []
        self.declarations = []
        self.variable_table = {}

        self.import_c_utils = []
        self.import_c_utils.append('from cstdio import *')
        self.import_c_utils.append('from cstring import *')
        self.run_cmd ='\n' + "if __name__ == '__main__':" + '\n' + '    ' + 'main()'

    def format_code(self, s):
        format_string = ''
        i = 0
        literals = ['=', '!', '>', '<', '+', '*', '/']
        while i < len(s):
            if s[i] in literals:
                if s[i + 1] == '=':
                    format_string += ' ' + s[i] + '=' + ' '
                    i = i + 2
                    continue
                elif s[i + 1] != '=':
                    format_string += ' ' + s[i] + ' '
                    i = i + 1
                    continue
            elif s[i] == '-':
                if s[i + 1] == '=':
                    format_string += ' -= '
                    i = i + 2
                    continue
                elif s[i + 1] != '=':
                    if not s[i + 1].isdigit():
                        format_string += ' - '
                        i = i + 1
                        continue
                    else:
                        format_string += s[i]
                        i = i + 1
                        continue
            elif s[i] == "'" or s[i] == '"':
                if s[i] == "'":
                    tmp = s.find("'", i + 1, len(s))
                else:
                    tmp = s.find('"', i + 1, len(s))
                format_string += s[i:tmp + 1]
                i = tmp + 1
                continue
            elif s[i] == ',':
                format_string += ', '
                i = i + 1
                continue
            else:
                format_string += s[i]
                i = i + 1
                continue
        return format_string

    def formatting(self, item, rank=-1):
        INDENT_STRING = '    '
        if type(item) == str:
            item = self.format_code(item)
            # 对于只声明不定义的变量需要补上=None
            if '(' not in item and ' ' not in item and '=' not in item and item != '' and item != 'break' \
                    and item != 'continue' and item != 'pass' and item != 'else:' and item != 'if' and item != 'return':
                item += ' = None'
            return INDENT_STRING * rank + item
        if type(item) == list:
            lines = []
            for i in item:
                lines.append(self.formatting(i, rank + 1))
            return '\n'.join(lines)

    def interpret(self):
        try:
            status, src_code = precompile(self.src_file)
            if not status:
                raise Exception('Precompile failed.')
                return
            tree = parser.parse(src_code)

            # semantic analysis
            raw_dst_code = self.process(tree)
            # formatting
            out = self.formatting(raw_dst_code)
            self.import_cmd = 'from cstdio import *' + '\n' + 'from cstring import *' + '\n'
            out = self.import_cmd + out
            dst_code = ''
            with open(self.dst_file, 'w+', encoding='utf-8') as f:
                f.write(out)
                f.write(self.run_cmd)

        except Exception as e:
            print(str(e))

    def function_declaration_judgement(self, tree):
        for child in tree.children:
            if isinstance(child, ASTLeafNode):
                return False
            elif child.ttype == 'direct_declarator':
                if len(child.children) > 1 and isinstance(child.children[1], ASTLeafNode) and child.children[1].value == '(':
                    return True
                else:
                    return False
            else:
                if self.function_declaration_judgement(child):
                    return True
        return False

    def process(self, tree):
        def get_def_dec(tree):
            if tree.ttype == 'function_definition':
                self.functions.append(tree)
            else:
                self.declarations.append(tree)
                
        while True:
            if tree.ttype == 'translation_unit':
                if len(tree.children) == 2:
                    get_def_dec(tree.children[1].children[0])
                    tree = tree.children[0]
                else:
                    get_def_dec(tree.children[0].children[0])
                    break
                    
        self.declarations = reversed(self.declarations)
        new_code = []
        for dec in self.declarations:
            if self.function_declaration_judgement(dec):
               continue
            self.extract_global_declaration(dec)
            code, _ = self.generate_code(dec, [], 'declaration')
            new_code.extend(code)
            new_code.append('')

        for function in self.functions:
            table_copy = copy.deepcopy(self.variable_table)
            self.name_replacement(function)
            self.variable_table = table_copy
            code, flag = self.generate_code(function, [], 'function')
            new_code.extend(code)
            new_code.append('')
        return new_code

    def extract_global_declaration(self, tree):
        if tree.ttype == 'struct_or_union_specifier' or isinstance(tree, ASTLeafNode):
            return
        for child in tree.children:
            if child.ttype == 'IDENTIFIER':
                alias = child.value
                self.global_variables.append(alias)
                self.variable_table[child.value] = [(alias, True)]
                child.value = alias
            
            else:
                self.extract_global_declaration(child)

    def leaf_node_translation(self, tree):
        match_token = {}
        match_token['||'] = [' or ']
        match_token['!'] = [' not ']
        match_token['&&'] = [' and ']
        match_token[';'] = ['']
        match_token['struct'] = ['class']
        try:
            match = match_token[tree.value]
        except:
            match = []
            match.append(tree.value)
        return match

    def get_flag(self, tree, flag_list):
        if tree.ttype == 'struct_or_union_specifier':
            return tree.children[1].value
        else:
            for flag in flag_list:
                if flag != '':
                    return flag
            return ''

    def generate_code(self, tree, stack, type):
        code_list, flag_list = [], []
        stack.append(tree.ttype)
        if isinstance(tree, ASTLeafNode):
            stack.pop()
            return self.leaf_node_translation(tree), ''
        for child in tree.children:
            code, flag = self.generate_code(child, stack, type)
            code_list.append(code)
            flag_list.append(flag)
        try:
            flag_ret = self.get_flag(tree, flag_list)
        except Exception as e:
            print(str(e))
        stack.pop()
        return self.code_translation(tree, code_list, flag_ret), flag_ret

    def name_replacement(self, tree, is_declarator=False):
        if isinstance(tree, ASTInternalNode):
            if tree.ttype == 'declarator':
                pass
            elif tree.ttype == 'primary_expression':
                for child in tree.children:
                    self.name_replacement(child, False)
            elif tree.ttype == 'struct_or_union_specifier':
                return
            elif tree.ttype == 'postfix_expression' and len(tree.children) == 3 \
                and isinstance(tree.children[2], ASTLeafNode) and tree.children[2].ttype == 'IDENTIFIER':
                for child in tree.children[:2]:
                    self.name_replacement(child, False)
                # 选择或循环语句，进入新一层作用域
            elif tree.ttype == 'iteration_statement' or tree.ttype == 'selection_statement':
                # 进入作用域，保存副本
                table_copy = copy.deepcopy(self.variable_table)
                for child in tree.children:
                    self.name_replacement(child, is_declarator)
                # 离开作用域，恢复变量表
                self.variable_table = table_copy
            else:
                for child in tree.children:
                    self.name_replacement(child, is_declarator)

        else:
            # 不是变量
            if tree.ttype != 'IDENTIFIER':
                return
            # 变量在变量表中
            if tree.value in self.variable_table.keys():
                # 是声明
                if is_declarator:
                    table = self.variable_table[tree.value]
                    # 不需要重命名
                    if len(table) == 0:
                        alias = tree.value + '_'
                        table.append((alias, False))
                        tree.value = alias
                    # 需要重命名并修改变量表
                    else:
                        alias = tree.value + '_' + str(len(table))
                        table.append((alias, False))
                        tree.value = alias
                # 不是声明
                else:
                    table = self.variable_table[tree.value]
                    # 需要重命名
                    if len(table) != 0:
                        last = table[-1][0]
                        tree.value = last
                    else:
                        tree.value = tree.value + '_'
            else:
                alias = tree.value + '_'
                self.variable_table[tree.value] = [(alias, False)]
                tree.value = alias
    
    def is_func_dec(self, dec):
        # whether a declaration is a function declaration
        for child in tree.children:
            if isinstance(child, ASTLeafNode):
                return False

    def code_translation(self, tree, code_list, flag_ret):
        # ++/--
        if (tree.ttype == 'unary_expression' and isinstance(tree.children[0], ASTLeafNode))\
                or (tree.ttype == 'postfix_expression' and len(tree.children) == 2):
            if tree.ttype == 'unary_expression':
                if tree.children[0].value == '++':
                    res = [code_list[1][0] + ' = ' + code_list[1][0] + '+1']
                elif tree.children[0].value == '--':
                    res = [code_list[1][0] + '=' + code_list[1][0] + '-1']
            else:
                if tree.children[1].value == '++':
                    res = [code_list[0][0] + '=' + code_list[0][0] + '+1']
                elif tree.children[1].value == '--':
                    res = [code_list[0][0] + '=' + code_list[0][0] + '-1']
            return res

        # return 语句
        elif tree.ttype == 'jump_statement' and tree.children[0].ttype == 'return':
            if len(tree.children) == 2:
                return ['return']
            elif len(tree.children) == 3:
                return [code_list[0][0] + ' ' + code_list[1][0]]

        # 选择语句
        elif tree.ttype == 'selection_statement':
            if len(tree.children) == 5:
                """
                if 条件:
                    代码块（缩进+1）
                """
                return ['if ' + code_list[2][0] + ':', code_list[4]]
            if len(tree.children) == 7:
                """
                if 条件:
                    代码块（缩进+1）
                else:
                    代码块（缩进+1）
                """
                return ['if ' + code_list[2][0] + ':', code_list[4], 'else:', code_list[6]]

        # 循环语句
        elif tree.ttype == 'iteration_statement':
            #  while {
            #      ...
            #  }
            if tree.children[0].value == 'while':
                """
                while 条件:
                    代码块（缩进+1）
                """
                return ['while ' + code_list[2][0] + ':', code_list[4]]
            #  for (...; ...; ...) {
            #      ...
            #  }
            if len(tree.children) == 7:
                """
                初始条件
                while 终止条件:
                    代码块（缩进+1）
                    迭代（缩进+1）
                """
                return [code_list[2][0], 'while ' + code_list[3][0] + ':', code_list[6], code_list[4]]

        # 语句块的换行
        elif tree.ttype == 'block_item_list':
            lst = []
            for code in code_list:
                for c in code:
                    lst.append(c)
            """
            语句1
            语句2
            ...
            """
            return lst

        # {}作用域 去除{}
        elif tree.ttype == 'compound_statement':
            if len(tree.children) == 3:
                """
                    代码块（缩进+1）
                """
                return code_list[1]
            # {}内为空，Python需要有 pass
            elif len(tree.children) == 2:
                """
                    pass（缩进+1）
                """
                return ['pass']

        # 函数声明, 返回值类型变为def,
        elif tree.ttype == 'function_definition':
            if len(tree.children) == 4:
                pass
            elif len(tree.children) == 3:
                function_body = []
                # 无脑加入所有全局变量
                for global_var in self.global_variables:
                    function_body.append('global ' + global_var)
                for code in code_list[2]:
                    function_body.append(code)
                """
                def 函数名:
                    函数体（缩进+1）
                """
                return ['def ' + code_list[1][0] + ':',
                        function_body]

        # 函数参数列表中参数类型的去除
        elif tree.ttype == 'parameter_declaration' and len(tree.children) == 2:
            """
            变量（没有类型）
            """
            return code_list[1]

        # 函数列表中数组“[]”的去除
        elif tree.ttype == 'direct_declarator' and len(tree.children) == 3 and tree.children[1].value == '[':
            """
            数组变量名
            """
            return [code_list[0][0]]

        # 形如int x, y=2;的声明中的x, y=2 , Python中需要分行
        elif tree.ttype == 'init_declarator_list':
            if len(tree.children) == 1:
                """
                变量名（=初始值）
                """
                return code_list[0]
            else:
                """
                变量名1（=初始值1）
                变量名2（=初始值2）
                """
                return [code_list[0][0],
                        code_list[2][0]]

        # 结构体变量的声明（形如struct A a;)
        elif tree.ttype == 'struct_or_union_specifier' and len(tree.children) == 2:
            """
            结构体名称
            """
            return code_list[1]

        # 结构体的定义（形如 struct A { int x; int y; };
        elif tree.ttype == 'struct_or_union_specifier' and len(tree.children) == 5:
            """
            class 结构体名称:
                成员变量（缩进+1）
            """
            return [code_list[0][0] + ' ' + code_list[1][0] + ':',
                    code_list[3]]

        # 结构体定义内的语句列表
        elif tree.ttype == 'struct_declaration_list':
            lst = []
            for code in code_list:
                for c in code:
                    lst.append(c)
            """
            成员变量1 = 初始值1
            成员变量2 = 初始值2
            ...
            """
            return lst

        # 声明语句
        if tree.ttype == 'declaration' or tree.ttype == 'struct_declaration':

            # 变量（非结构体）声明，去除变量类型和分号
            if len(tree.children) == 3 and flag_ret == '':
                return code_list[1] # 返回变量名

            # 结构体变量声明
            elif len(tree.children) == 3 and flag_ret != '':
                # flag_ret 为结构体名称
                if flag_ret != code_list[0][0]:
                    result = code_list[0]
                else:
                    result = []
                for class_obj in code_list[1]:
                    result.append(class_obj + '=' + flag_ret + '()')

                # 结构体数组的处理
                if len(result) == 1:
                    tmp = result[0]
                    if tmp.find('=') != tmp.rfind('='):
                        tmp_2 = tmp.split('=')[2]
                        tmp_2 = tmp_2.lstrip()
                        tmp = tmp.split('=')[0] + '=' + tmp.split('=')[1]
                        tmp = tmp[0:tmp.find('[') + 1] + tmp_2 + ' for i in range(' + tmp[tmp.find('*') + 1:] + ')]'
                        tmp = tmp.rstrip()
                        result = []
                        result.append(tmp)
                return result

            elif len(tree.children) == 2:
                return code_list[0]

        # 数组的声明与定义，如：
        # int s[10]; == > s = [0] * 10
        # int s[5] = {1,2,3}; ==>  s = [1,2,3,0,0]
        # char s[5] = "abc"; ==>  s = ['a','b','c',0,0]
        elif tree.ttype == 'direct_declarator' and len(tree.children) == 4 and \
                isinstance(tree.children[2], ASTInternalNode) and \
                tree.children[2].ttype == 'assignment_expression':
            return [code_list[0][0] + '=[' + 'None' + ']*' + code_list[2][0]] # 数组名 = [None] * 长度

        elif tree.ttype == 'init_declarator' and len(tree.children) == 3 and code_list[0][0].find('[') >= 0:
            tmp = code_list[0][0]  # s[0]*5
            index_1 = tmp.find('[')
            left = tmp[:index_1 - 1]  # s
            length = code_list[0][0].split('*')[1]  # 5

            # 字符数组 "..."初始化
            if code_list[2][0].find('"') >= 0:
                tmp = code_list[2][0].strip('"')  # "abc"
                result = [left + '=[None]*' + length]
                for i, c in enumerate(tmp):
                    result.append(left + '[' + str(i) + ']="' + c + '"')
                """
                数组名 = [None] * 长度
                数组名[0] = 初始值1 ("字符")
                数组名[1] = 初始值2
                ...
                """
                return result

            # 其他类型的数组 {...}初始化
            else:
                tmp = code_list[2][0].split(',')
                result = [left + '=[None]*' + length]
                for i, c in enumerate(tmp):
                    result.append(left + '[' + str(i) + ']=' + c)
                """
                数组名 = [None] * 长度
                数组名[0] = 初始值1
                数组名[1] = 初始值2
                ...
                """
                return result

        # 去除数组的[]
        elif tree.ttype == 'initializer' and len(tree.children) == 3:
            return code_list[1] # 返回[]中的值

        # 其他情况
        else:
            lst = []
            flag = True
            for code in code_list:
                if len(code) != 1:
                    flag = False
            if flag:
                s = ''
                for code in code_list:
                    s += code[0]
                lst.append(s)
            else:
                for code in code_list:
                    lst.extend(code)
            return lst

    
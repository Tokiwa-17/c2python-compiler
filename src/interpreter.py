from preprocessing import precompile
from yacc import parser
#from c_utils import c_utils
from ast_ import ASTLeafNode, ASTInternalNode

class Interpreter:
    def __init__(self, src_file, dst_file):
        self.src_file = src_file
        self.dst_file = dst_file
        #print(src_file)
        if self.src_file.split('.')[-1] != 'c':
            raise Exception('The type of source file is incorrect.')
        if self.dst_file.split('.')[-1] != 'py':
            raise Exception('The type of destination file is incorrect.')

        self.global_variables = []
        self.functions = []
        self.declarations = []
        self.variable_table = {}

        # TODO import
        self.import_c_utils = []
        self.import_c_utils.append('from cstdio import *')
        self.import_c_utils.append('from cstring import *')
        self.run_cmd = '''
        if __name__ == '__main__':
            main_0()
        '''


    def interpret(self):
        try:
            status, src_code = precompile(self.src_file)
            if not status:
                raise Exception('Precompile failed.')
                return
            tree = parser.parse(src_code)

            # TODO: semantic analysis
            raw_dst_code = self.process(tree)
            # TODO: format
            dst_code = ''

            # ouput
            with open(self.dst_file, 'w+', encoding='utf-8') as f:
                f.write(dst_code)
        except Exception as e:
            print(str(e))

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
            # TODO: function declaration
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
                alias = child.value + '_'
                self.global_variables.append(alias)
                self.variable_table[child.value] = [(alias, True)]
                child.value = alias
            
            else:
                self.extract_global_declaration(child)

    def leaf_node_translation(self, tree):
        if tree.value == ';':
            return ['']
        elif tree.value == '&&':
            return [' and ']
        elif tree.value == '||':
            return [' or ']
        elif tree.value == '!':
            return [' not ']
        elif tree.value == 'true':
            return ['True']
        elif tree.value == 'false':
            return ['False']
        elif tree.value == 'struct':
            return ['class']
        else:
            return [tree.value]

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
        return self.code_compose(tree, code_list, flag_ret), flag_ret

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
            if tree.key != 'IDENTIFIER':
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
            pass

    def code_compose(self, tree, code_list, flag_ret):
        pass
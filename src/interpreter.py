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

    def formatting(self, item, rank=-1):
        if type(item) == str:
            if '(' not in item and ' ' not in item and '=' not in item and item != '' and item != 'break' \
                    and item != 'continue' and item != 'pass' and item != 'else:' and item != 'if' and item != 'return':
                item += ' = None'
            return '    ' * rank + item
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
        match_token['true'] = ['True']
        match_token['false'] = ['False']
        try:
            match = match_token[tree.value]
        except:
            match = []
            match.append(tree.value)
        return match

    def get_struct(self, tree, struct_list):
        if tree.ttype == 'struct_or_union_specifier':
            return tree.children[1].value
        else:
            for struct in struct_list:
                if struct != '':
                    return struct
            return ''

    def generate_code(self, tree, stack, type):
        code_list, struct_list = [], []
        stack.append(tree.ttype)
        if isinstance(tree, ASTLeafNode):
            stack.pop()
            return self.leaf_node_translation(tree), ''
        for child in tree.children:
            code, struct = self.generate_code(child, stack, type)
            code_list.append(code)
            struct_list.append(struct)
        try:
            struct_ret = self.get_struct(tree, struct_list)
        except Exception as e:
            print(str(e))
        stack.pop()
        return self.code_translation(tree, code_list, struct_ret), struct_ret

    def is_func_dec(self, dec):
        # whether a declaration is a function declaration
        for child in tree.children:
            if isinstance(child, ASTLeafNode):
                return False

    def code_translation(self, tree, code_list, struct_ret):
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

        elif tree.ttype == 'jump_statement' and tree.children[0].ttype == 'return':
            if len(tree.children) == 2:
                return ['return']
            elif len(tree.children) == 3:
                return [code_list[0][0] + ' ' + code_list[1][0]]

        elif tree.ttype == 'selection_statement':
            if len(tree.children) == 5:
                return ['if ' + code_list[2][0] + ':', code_list[4]]
            if len(tree.children) == 7:
                return ['if ' + code_list[2][0] + ':', code_list[4], 'else:', code_list[6]]

        elif tree.ttype == 'iteration_statement':
            if tree.children[0].value == 'while':
                return ['while ' + code_list[2][0] + ':', code_list[4]]
            if len(tree.children) == 7:
                return [code_list[2][0], 'while ' + code_list[3][0] + ':', code_list[6], code_list[4]]

        elif tree.ttype == 'block_item_list':
            lst = []
            for code in code_list:
                for c in code:
                    lst.append(c)
            return lst

        elif tree.ttype == 'compound_statement':
            if len(tree.children) == 3:
                return code_list[1]
            elif len(tree.children) == 2:
                return ['pass']

        elif tree.ttype == 'function_definition':
            if len(tree.children) == 4:
                pass
            elif len(tree.children) == 3:
                function_body = []
                for global_var in self.global_variables:
                    function_body.append('global ' + global_var)
                for code in code_list[2]:
                    function_body.append(code)
                return ['def ' + code_list[1][0] + ':',
                        function_body]

        elif tree.ttype == 'parameter_declaration' and len(tree.children) == 2:
            return code_list[1]

        elif tree.ttype == 'direct_declarator' and len(tree.children) == 3 and tree.children[1].value == '[':
            return [code_list[0][0]]

        elif tree.ttype == 'init_declarator_list':
            if len(tree.children) == 1:
                return code_list[0]
            else:
                return [code_list[0][0],
                        code_list[2][0]]

        elif tree.ttype == 'struct_or_union_specifier' and len(tree.children) == 2:
            return code_list[1]

        elif tree.ttype == 'struct_or_union_specifier' and len(tree.children) == 5:
            return [code_list[0][0] + ' ' + code_list[1][0] + ':',
                    code_list[3]]

        elif tree.ttype == 'struct_declaration_list':
            lst = []
            for code in code_list:
                for c in code:
                    lst.append(c)
            return lst

        if tree.ttype == 'declaration' or tree.ttype == 'struct_declaration':
            if len(tree.children) == 3 and struct_ret == '':
                return code_list[1] # 返回变量名
            elif len(tree.children) == 3 and struct_ret != '':
                if struct_ret != code_list[0][0]:
                    result = code_list[0]
                else:
                    result = []
                for class_obj in code_list[1]:
                    result.append(class_obj + '=' + struct_ret + '()')
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

        elif tree.ttype == 'direct_declarator' and len(tree.children) == 4 and \
                isinstance(tree.children[2], ASTInternalNode) and \
                tree.children[2].ttype == 'assignment_expression':
            return [code_list[0][0] + '=[' + 'None' + ']*' + code_list[2][0]] # 数组名 = [None] * 长度

        elif tree.ttype == 'init_declarator' and len(tree.children) == 3 and code_list[0][0].find('[') >= 0:
            tmp = code_list[0][0]  # s[0]*5
            index_1 = tmp.find('[')
            left = tmp[:index_1 - 1]  # s
            length = code_list[0][0].split('*')[1]  # 5

            if code_list[2][0].find('"') >= 0:
                tmp = code_list[2][0].strip('"')  # "abc"
                result = [left + '=[None]*' + length]
                for i, c in enumerate(tmp):
                    result.append(left + '[' + str(i) + ']="' + c + '"')
                return result

            else:
                tmp = code_list[2][0].split(',')
                result = [left + '=[None]*' + length]
                for i, c in enumerate(tmp):
                    result.append(left + '[' + str(i) + ']=' + c)
                return result

        elif tree.ttype == 'initializer' and len(tree.children) == 3:
            return code_list[1] # 返回[]中的值

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

    
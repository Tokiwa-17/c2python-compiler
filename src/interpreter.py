from preprocessing import precompile
from yacc import parser

class Interpreter:
    def __init__(self, src_file, dst_file):
        self.src_file = src_file
        self.dst_file = dst_file
        #print(src_file)
        if self.src_file.split('.')[-1] != 'c':
            raise Exception('The type of source file is incorrect.')
        if self.dst_file.split('.')[-1] != 'py':
            raise Exception('The type of destin`ation file is incorrect.')

        self.global_variables = []
        self.functions = []
        self.declarations = []

        # :TODO c_utils

    def interpret(self):
        try:
            status, src_code = precompile(self.src_file)
            if not status:
                raise Exception('Precompile failed.')
                return
            tree = parser.parse(src_code)

            # TODO: semantic analysis
            raw_dst_code = self.semantic_process(tree)
            # TODO: format
            dst_code = ''

            # ouput
            with open(self.dst_file, 'w+', encoding='utf-8') as f:
                f.write(dst_code)
        except Exception as e:
            print(str(e))

    def semantic_process(self, tree):
        pass


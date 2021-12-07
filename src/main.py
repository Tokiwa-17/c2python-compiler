import sys
from interpreter import Interpreter


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 2:
        raise Exception('Parameter number error.')
    src_file = sys.argv[1]
    dst_file = '.'.join(sys.argv[1].split('.')[:-1]) + '.py'
    interpreter = Interpreter(src_file, dst_file)
    interpreter.interpret()


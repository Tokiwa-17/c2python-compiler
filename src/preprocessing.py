
def remove_side_whitespace(str):
    str = str.strip(' ')
    str = str.strip('\t')
    str = str.strip('\n')
    str = str.strip('\r')
    return str

def precompile(filename):
    """Fetches #define and #include command(ignore standard library).
    Args:
        filename: c file.
    Returns:
        status: indicates that precompile is successful or not.
        code: code without #define and #include command.
    """
    try:
        f = open(filename, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
    except:
        raise Exception('File not exists.')

    define_list = []
    include_list = []
    remove_line_idx = []
    for idx, line in enumerate(lines):
        line = remove_side_whitespace(line)
        lines[idx] = line
        # if the line is None
        if len(line) <= 0:
            #lines.pop(idx)
            remove_line_idx.append(idx)
            continue

        if line[0] == '#':
            type = line.split()[0]
            if type == '#define':
                define_list.append((line[1], words[2]))
                # TODO:
            elif type == '#include':
                pass
                # TODO:
            else:
                raise KeyError

            remove_line_idx.append(idx)
            continue

    remove_line_idx.sort(reverse=True)
    for line_idx in remove_line_idx:
        lines.pop(line_idx)

    code = '\n'.join(lines)
    # handle define
    # TODO:

    # handle include
    # TODO:

    return True, code

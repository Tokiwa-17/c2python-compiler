# -*- coding=utf-8 -*-

class ASTNode:
    def __init__(self, ttype):
        self.ttype = ttype


class ASTLeafNode(ASTNode):
    def __init__(self, ttype, value: str):
        ASTNode.__init__(self, ttype)
        self.value = str(value)
        
    def __str__(self):
        return self.value


class ASTInternalNode(ASTNode):
    def __init__(self, ttype, children):
        ASTNode.__init__(self, ttype)
        # literals -> tokens
        self.children = [c if isinstance(c, ASTNode) else ASTLeafNode(str(c), str(c)) for c in children]
    
    def __str__(self):
        return ''.join(map(str, self.children))

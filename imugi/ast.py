from typing import (
    List,
    Union,
)


class ASTNode(object):
    def __init__(self, name: str, kind: str, value: Union[str, None]=None):
        """Node for AST

        Args:
            name (str): Node name eg. variable name
            kind (str): Node type eg. int, str
            value (str, optional): eg. variable value

        """
        self.name = name
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f'ASTNode({self.name}, {self.kind}, {self.value})'


class PrototypeAST(object):
    def __init__(self, name: str, args: List[ASTNode], ret: str):
        """Function prototype AST

        Args:
            name (str): Function name
            args (list): List of ASTNode that function arguments information
            ret (str): Function return type

        """
        self.name = name
        self.args = args
        self.ret = ret

    def __repr__(self):
        return f'PrototypeAST({self.name}, {self.args}, {self.ret})'


class FunctionAST(object):
    def __init__(self, proto: PrototypeAST):
        """Function AST

        Args:
            proto (PrototypeAST): Function prototype AST

        Todo:
            * support body ast

        """
        self.proto: PrototypeAST = proto

    def __repr__(self):
        return f'FunctionAST({self.proto}'

from typing import (
    List,
    Union,
)


class ASTNode:
    def __init__(self, name: str, kind: str, value: Union[str, None]=None):
        self.name = name
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f'ASTNode({self.name}, {self.kind}, {self.value})'


class PrototypeAST:
    def __init__(self, name: str, args: List[ASTNode], ret: str):
        self.name = name
        self.args = args
        self.ret = ret

    def __repr__(self):
        return f'PrototypeAST({self.name}, {self.args}, {self.ret})'

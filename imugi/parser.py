from tokenize import (
    ENCODING,
    NAME,
    NEWLINE,
    OP,
    TokenInfo,
    tokenize,
)
from typing import (
    List,
    Union,
)

from imugi.ast import (
    ASTNode,
    PrototypeAST,
)

PRIMITIVE_TYPE = [
    'int',
    'float',
]


class Parser:
    def __init__(self, source):
        self.token_generator = tokenize(source)
        self.cursor_token: (TokenInfo, None) = None

    def parse(self):
        self.next_token()
        token_kind = self.get_token_kind()
        if token_kind == ENCODING:
            self.next_token()
            token_kind = self.get_token_kind()

        if token_kind == NAME:
            return self.parse_name()

    def parse_name(self):
        token_val = self.get_token_val()
        if token_val == 'def':
            return self.parse_def()

    def parse_def(self):
        self.next_token()
        proto_ast = self.parse_proto()
        # TODO: parse body and return FunctionAST
        return proto_ast

    def parse_proto(self) -> PrototypeAST:
        name = self.get_token_val()
        self.next_token()

        self.check(OP, '(')
        args = self.parse_args()
        self.check(OP, ')')

        self.check(OP, '->')
        ret = self.get_token_val()
        self.check(NAME, ret)
        self.check(OP, ':')
        self.check(NEWLINE, '\n')

        return PrototypeAST(name, args, ret)

    def parse_args(self) -> List[ASTNode]:
        args = []
        # TODO: Support default kwarg and also support tuple too
        # TODO: Support non-static type
        while (self.get_token_kind() != OP) and (self.get_token_val() != ')'):
            arg_name = self.get_token_val()
            self.check(NAME, arg_name)

            self.check(OP, ':')
            arg_type = self.get_token_val()
            if arg_type not in PRIMITIVE_TYPE:
                raise Exception(f'{arg_type} is not support yet')
            self.check(NAME, arg_type)

            if self.get_token_kind() == OP and self.get_token_val() == ',':
                self.next_token()

            args.append(ASTNode(arg_name, arg_type))

        return args

    def get_token_kind(self) -> Union[int, None]:
        if self.cursor_token is None:
            return None

        token_kind, _, _, _, _ = self.cursor_token
        return token_kind

    def get_token_val(self) -> Union[str, None]:
        if self.cursor_token is None:
            return None

        _, token_val, _, _, _ = self.cursor_token
        return token_val

    def check(self, kind, value):
        token_kind = self.get_token_kind()
        if self.get_token_kind() != kind:
            raise Exception(f'Expected: {kind}, get: {token_kind} at:{self.cursor_token.start}:{self.cursor_token.end}')

        token_val = self.get_token_val()
        if self.get_token_val() != value:
            raise Exception(f'Expected: {value}, get: {token_val} at:{self.cursor_token.start}:{self.cursor_token.end}')

        self.next_token()

    def next_token(self):
        self.cursor_token = next(self.token_generator)

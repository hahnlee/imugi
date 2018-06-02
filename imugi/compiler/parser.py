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

from imugi.compiler.ast import (
    ASTNode,
    FunctionAST,
    PrototypeAST,
)

PRIMITIVE_TYPE = [
    'int',
    'float',
]


class Parser(object):
    def __init__(self, source):
        self.token_generator = tokenize(source)
        self.cursor_token: Union[TokenInfo, None] = next(self.token_generator)

    def parse(self):
        """parse source to generate AST
        """
        token_kind = self.get_token_kind()
        if token_kind == ENCODING:
            self.next_token()
            token_kind = self.get_token_kind()

        if token_kind == NAME:
            return self.parse_name()

    def parse_name(self):
        """parse when token kind is NAME and def or class

        Todo:
            * parse when class
        """
        token_val = self.get_token_val()
        if token_val == 'def':
            return self.parse_def()
        elif token_val == 'class':
            raise Exception('class is not support yet')
        raise SyntaxError(f'Expected: def or class, get: {token_val}')

    def parse_def(self) -> FunctionAST:
        """parse function for when def

        Returns:
            FunctionAST: Function AST

        Todo:
            * parse body

        """
        self.next_token()
        proto_ast = self.parse_proto()
        return FunctionAST(proto_ast)

    def parse_proto(self) -> PrototypeAST:
        """parse function prototype

        Returns:
            PrototypeAST: Function prototype ast

        Raises:
            SyntaxError: When wrong python syntax or no return type

        """
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
        """parse and get function arguments

        Returns:
            list: List of ASTNode that include arguments data

        Raises:
            SyntaxError: When wrong python syntax or does not has type information

        Todo:
            * Support default kwarg and also support tuple too
            * Support non-static type

        """
        args = []
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
        """Provide cursor token's token type

        Returns:
            int: Token type
            None: When cursor_token is None (case when no more token)

        """
        if self.cursor_token is None:
            return None

        token_kind, _, _, _, _ = self.cursor_token
        return token_kind

    def get_token_val(self) -> Union[str, None]:
        """Provide cursor token's token value

        Returns:
            str: Token value
            None: When cursor_token is None (case when no more token)

        """
        if self.cursor_token is None:
            return None

        _, token_val, _, _, _ = self.cursor_token
        return token_val

    def check(self, kind: int, value: str):
        """Check cursor token's kind and value with given arguments. if both are same then move cursor to next token

        Args:
            kind (int): Expected token kind
            value (str): Expected token value

        Raises:
            SyntaxError: if token kind or value are different.

        """
        token_kind = self.get_token_kind()
        if self.get_token_kind() != kind:
            raise SyntaxError(f'Expected: {kind}, get: {token_kind}')

        token_val = self.get_token_val()
        if self.get_token_val() != value:
            raise SyntaxError(f'Expected: {value}, get: {token_val}')

        self.next_token()

    def next_token(self):
        self.cursor_token = next(self.token_generator)

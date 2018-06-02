from typing import (
    Union,
)

from llvmlite import (
    ir,
)

from imugi.compiler.ast import (
    ASTNode,
    FunctionAST,
    PrototypeAST,
)


class CodeGen(object):
    def __init__(self):
        self.module: ir.Module = ir.Module()

    def get_node_type(self, node: ASTNode) -> Union[ir.IntType, ir.FloatType]:
        """Provide a LLVM IR type corresponding to ASTNode

        Args:
            node (ASTNode): ASTNode that try to get LLVM IR type

        Returns:
            ir.Type: LLVM IR type corresponding to ASTNode

        """
        return self.get_type(node.kind)

    def get_type(self, kind: str) -> Union[ir.IntType, ir.FloatType]:
        """Provide a LLVM IR type corresponding to kind

        Args:
            kind (str): Type information

        Returns:
            ir.Type: LLVM IR type corresponding to kid

        Raises:
            Exception: when type does not support yet

        """
        if kind == 'int':
            return ir.IntType(bits=32)
        elif kind == 'float':
            return ir.FloatType()
        raise Exception(f'{kind} is not support yet')

    def gen_proto_type(self, node: PrototypeAST) -> ir.Function:
        """IR Generator for PrototypeAST

        Args:
            node (PrototypeAST): PrototypeAST that become ir code

        Returns:
            ir.Function: Function LLVM IR code

        """
        func_name: str = node.name
        func_return_type = self.get_type(node.ret)
        func_args_types = [self.get_node_type(arg_node) for arg_node in node.args]
        func_type = ir.FunctionType(func_return_type, func_args_types)
        func = ir.Function(self.module, func_type, func_name)
        return func

    def gen_func_type(self, node: FunctionAST) -> ir.Function:
        """IR Generator for FunctionAST

        Args:
            node (FunctionAST): Function prototype ast

        Returns:
            ir.Function: Function LLVM IR code

        Todo:
            * Support entry block
            * Generate IR code for function body

        """
        func: ir.Function = self.gen_proto_type(node.proto)
        return func

from llvmlite import (
    ir,
)

from imugi.ast import (
    ASTNode,
    PrototypeAST,
)


class CodeGen:
    def __init__(self):
        self.module: ir.Module = ir.Module()

    def get_node_type(self, node: ASTNode):
        return self.get_type(node.kind)

    def get_type(self, kind: str):
        if kind == 'int':
            return ir.IntType(bits=64)
        elif kind == 'float':
            return ir.FloatType()
        raise Exception(f'{kind} is not support yet')

    def gen_proto_type(self, node: PrototypeAST):
        func_name = node.name
        func_return_type = self.get_type(node.ret)
        func_args_types = [self.get_node_type(arg_node) for arg_node in node.args]
        func_type = ir.FunctionType(func_return_type, func_args_types)
        func = ir.Function(self.module, func_type, func_name)
        return func

    def gen_func_type(self, node):
        func = self.gen_proto_type(node)
        # TODO: support entry block
        return func

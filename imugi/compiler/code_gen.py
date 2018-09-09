from ast import (
    FunctionDef,
    NodeVisitor,
    Mult,
    Add,
)
from typing import (
    Union,
)

from llvmlite import (
    ir,
    binding as llvm,
)

from imugi.compiler.types import (
    char_pointer,
    i8,
    i64,
)
from imugi.compiler.utils import (
    ObjectiveCUtil,
)


class CodeGen(NodeVisitor):
    llvm.initialize()
    llvm.initialize_native_target()

    module = ir.Module(name=__file__)
    module.triple = llvm.get_default_triple()

    builder = None
    is_class = False
    module_name = '__main__'

    func_symtab = {}
    class_symtab = {}

    def set_objc(self):
        ObjectiveCUtil.set_objc_class(self.module)
        self.object_class = self.module.context.get_identified_type('object_class')
        self.Class = ir.PointerType(self.object_class)
        func_type = ir.FunctionType(ir.PointerType(self.object_class), [self.Class, char_pointer, i64])
        self.objc_allocateClassPair = ir.Function(self.module, func_type, name='objc_allocateClassPair')

    def visit_top(self, node):
        self.set_objc()
        func_name = 'main'
        func_args_types = []
        func_return_type = i64
        func_type = ir.FunctionType(func_return_type, func_args_types)
        func = ir.Function(self.module, func_type, func_name)
        bb_entry = func.append_basic_block('entry')
        global_builder = ir.IRBuilder(bb_entry)
        self.builder = global_builder

        for ast_node in node.body:
            self.visit(ast_node)
            self.builder = global_builder

        self.builder.ret(ir.Constant(i64, 0))

    def visit_ClassDef(self, node):
        c_str_val = ir.Constant(ir.ArrayType(i8, len(node.name)), bytearray(node.name.encode('utf8')))
        c_str = self.builder.alloca(c_str_val.type)
        self.builder.store(c_str_val, c_str)
        fmt_arg = self.builder.bitcast(c_str, char_pointer)
        self.builder.call(
            self.objc_allocateClassPair,
            [
                ir.Constant(self.Class, self.Class.null),
                fmt_arg,
                ir.Constant(i64, 0),
            ],
        )

    def visit_FunctionDef(self, node: FunctionDef):
        func_name = node.name
        func_args_types = [self.get_type(arg.annotation.id) for arg in node.args.args]
        func_return_type = self.get_type(node.returns.id)
        func_type = ir.FunctionType(func_return_type, func_args_types)
        func = ir.Function(self.module, func_type, func_name)

        bb_entry = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(bb_entry)

        for i, arg in enumerate(func.args):
            arg.name = node.args.args[i].arg
            alloca = self.builder.alloca(self.get_type(node.args.args[i].annotation.id), name=arg.name)
            self.builder.store(arg, alloca)
            self.func_symtab[arg.name] = alloca

        for body in node.body:
            self.visit(body)

    def visit_Assign(self, node):
        val_type, value = self.visit(node.value)
        # TODO: Support tuple assign
        target = node.targets[0]
        if target.id in self.func_symtab:
            var_addr = self.func_symtab[node.target.id]
        else:
            var_addr = self.builder.alloca(val_type, name=target.id)
            self.func_symtab[target.id] = var_addr
        return val_type, self.builder.store(value, var_addr)

    def visit_Name(self, node):
        var_addr = self.func_symtab[node.id]
        return var_addr.type, self.builder.load(var_addr, node.id)

    def visit_Num(self, node):
        if type(node.n) == int:
            return i64, ir.Constant(i64, node.n)

    def visit_BinOp(self, node):
        lhs_type, lhs = self.visit(node.left)
        rhs_type, rhs = self.visit(node.right)

        if type(node.op) == Mult:
            return lhs_type, self.builder.mul(lhs, rhs)
        if type(node.op) == Add:
            return rhs_type, self.builder.add(lhs, rhs)

    def visit_Return(self, node):
        _, retval = self.visit(node.value)
        self.builder.ret(retval)

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
            return i64
        elif kind == 'float':
            return ir.FloatType()
        elif kind == 'double':
            return ir.DoubleType()
        raise Exception(f'{kind} is not support yet')

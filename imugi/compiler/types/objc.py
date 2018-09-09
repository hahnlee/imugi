from llvmlite import (
    ir,
)

from .llvm_type import (
    char_pointer,
    i32,
)


objc_ivar = ir.LiteralStructType((
    char_pointer,  # char * ivar_name
    char_pointer,  # char * ivar_type
    i32,  # int ivar_offset
    i32,  # int space
), True)


objc_ivar_list = ir.LiteralStructType((
    i32,
    i32,
    ir.ArrayType(objc_ivar, 1),
), True)

from llvmlite import (
    ir,
)


i8 = ir.IntType(bits=8)
i32 = ir.IntType(bits=32)
i64 = ir.IntType(bits=64)

char_pointer = ir.PointerType(i8)

from sys import (
    platform,
)

from llvmlite import (
    ir,
)

from imugi.compiler.types import (
    char_pointer,
    i64,
    objc_ivar_list,
)


class ObjectiveCUtil(object):
    @staticmethod
    def get_objc_runtime_path() -> str:
        if platform == 'darwin':
            return '/usr/lib/libobjc.A.dylib'
        raise Exception(f'{platform} is not support yet')

    @staticmethod
    def set_objc_class(module: ir.Module):
        object_class = module.context.get_identified_type('object_class')
        objc_class = object_class.as_pointer()
        object_class.set_body(
            objc_class,  # Class
            char_pointer,  # char * _Nonnull name
            i64,  # long version
            i64,  # long info
            i64,  # long instance_size
            objc_ivar_list,
        )

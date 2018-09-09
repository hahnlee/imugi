import ast

from argparse import (
    ArgumentParser,
    FileType,

)
from subprocess import (
    call,
)
from sys import (
    platform,
)

from imugi.compiler.code_gen import (
    CodeGen,
)
from imugi.compiler.utils import (
    ObjectiveCUtil,
)


def main() -> int:
    if platform != 'darwin':
        print('only x86_64 macOS are supported')
        return 1

    # set and parse args
    parser = ArgumentParser(description="ikjMatrix multiplication")
    parser.add_argument('-i', '--input', dest='file', type=FileType('rb'), required=True)
    parser.add_argument('-o', '--output', dest='output_file_name', type=str, default='a')
    args = parser.parse_args()

    # parse and generate ir
    tree = ast.parse(args.file.read())

    code_gen = CodeGen()
    code_gen.visit_top(tree)

    with open(f'{args.output_file_name}.ll', 'w') as f:
        f.write(str(code_gen.module))

    call(['llc', f'{args.output_file_name}.ll'])

    call([
        'clang', f'{args.output_file_name}.s',
        '-O', ObjectiveCUtil.get_objc_runtime_path(),
        '-o', f'{args.output_file_name}.out',
    ])
    return 0


if __name__ == '__main__':
    exit(main())

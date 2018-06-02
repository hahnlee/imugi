from argparse import (
    ArgumentParser,
    FileType,
)
from sys import (
    platform,
)

from imugi.compiler.code_gen import (
    CodeGen,
)
from imugi.compiler.parser import (
    Parser,
)


def main() -> int:
    if platform not in ['darwin', 'linux', ]:
        print('only x86_64 Linux and macOS are supported')
        return 1

    # set and parse args
    parser = ArgumentParser(description="ikjMatrix multiplication")
    parser.add_argument('-i', '--input', dest='file', type=FileType('rb'), required=True)
    args = parser.parse_args()

    # parse and generate ir
    parser = Parser(args.file.readline)
    ast = parser.parse()
    code_gen = CodeGen()
    _ = code_gen.gen_func_type(ast)
    return 0


if __name__ == '__main__':
    exit(main())

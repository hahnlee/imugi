import unittest
from io import (
    BytesIO,
)

from imugi.parser import (
    Parser,
)


class TestParser(unittest.TestCase):
    def get_bytes(self, source_code: str) -> BytesIO:
        return BytesIO(source_code.encode('utf-8'))

    def test_correct_function(self):
        source_code = 'def test(a: int) -> int:\n'
        parser = Parser(self.get_bytes(source_code).readline)
        parser.parse()

    def test_multi_args(self):
        source_code = 'def test(a: int, b: int) -> int:\n'
        parser = Parser(self.get_bytes(source_code).readline)
        parser.parse()

    def test_none_args(self):
        source_code = 'def test() -> int:\n'
        parser = Parser(self.get_bytes(source_code).readline)
        parser.parse()

    def test_empty_args_include_comma_function(self):
        source_code = 'def test(,) -> int:\n'
        parser = Parser(self.get_bytes(source_code).readline)
        self.assertRaises(Exception, parser.parse)

import unittest

import ast
import gast
import sys


class UnparserTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None

    def assertUnparse(self, code):
        normalized_code = ast.unparse(ast.parse(code))
        tree = gast.parse(normalized_code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        unparsed = gast.unparse(tree)
        self.assertEqual(normalized_code, unparsed)

    def test_FunctionDef(self):
        self.assertUnparse('def foo(x, y): return x, y')

    def test_BinaryOp(self):
        self.assertUnparse('1 + 3')

    if sys.version_info >= (3, 12):

        def test_TypeParameter(self):
            self.assertUnparse('type x[T] = list[T]')


if sys.version_info < (3, 9):
    del UnparserTestCase

if __name__ == '__main__':
    unittest.main()

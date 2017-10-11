import unittest

import ast
import gast
import sys


class CompatTestCase(unittest.TestCase):

    if sys.version_info.major == 2:

        def test_With(self):
            code = 'with open("any"): pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_TryFinally(self):
            code = 'try:pass\nfinally:pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_TryExcept(self):
            code = 'try:pass\nexcept e:pass\nelse:pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_Raise(self):
            codes = ('raise Exception',
                     'raise "Exception"',
                     'raise Exception, "err"',
                     'raise Exception("err")',
                     'raise E, V, T',)

            for code in codes:
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_Call(self):
            code = 'foo(x, y=1, *args, **kwargs)'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

    else:

        def test_ArgAnnotation(self):
            code = 'def foo(x:int): pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_KeywordOnlyArgument(self):
            code = 'def foo(*, x=1): pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_TryExceptNamed(self):
            code = 'try:pass\nexcept e as f:pass\nelse:pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        def test_Call(self):
            code = 'foo(x, y=1, *args, **kwargs)'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')

        if sys.version_info.minor >= 6:

            def test_FormattedValue(self):
                code = 'e = 1; f"{e}"'
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')

            def test_JoinedStr(self):
                code = 'e = 1; f"e = {e}"'
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')


if __name__ == '__main__':
    unittest.main()

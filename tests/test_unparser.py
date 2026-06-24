import unittest

import ast
import gast
import sys


class UnparserTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None

    def assertUnparse(self, code, parse_only=False):
        normalized_code = ast.unparse(ast.parse(code))
        tree = gast.parse(normalized_code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        unparsed = gast.unparse(tree)
        if not parse_only:
            self.assertEqual(normalized_code, unparsed)

    def test_FunctionDef(self):
        self.assertUnparse('def foo(x, y): return x, y')

    def test_BinaryOp(self):
        self.assertUnparse('1 + 3')

    def test_ast_py(self):
        with open(ast.__file__) as astfd:
            self.assertUnparse(astfd.read(),
                               parse_only=sys.version_info < (3, 12))

    if sys.version_info >= (3, 12):

        def test_TypeParameter(self):
            self.assertUnparse('type x[T] = list[T]')

        def test_TemplateStr_format_spec(self):
            val_node = gast.Name(id='value', ctx=gast.Load(), annotation=None, type_comment=None)
            format_spec_node = gast.TemplateStr(values=[
                gast.Constant(value='format', kind=None)
            ])
            interp_node = gast.Interpolation(
                value=val_node,
                str='value',
                conversion=-1,
                format_spec=format_spec_node
            )
            tree = gast.TemplateStr(values=[interp_node])
            unparsed = gast.unparse(tree)
            self.assertEqual(unparsed, "t'{value:format}'")

        def test_JoinedStr_format_spec_quotes(self):
            self.assertUnparse("f\"hello {val:'format'}\"")


    if sys.version_info >= (3, 10):

        def test_MatchMapping(self):
            self.assertUnparse('''
match obj:
    case {"x": 1}:
        pass
''')

        def test_MatchClass(self):
            self.assertUnparse('''
match obj:
    case Point(1, y=2):
        pass
''')


if sys.version_info < (3, 9):
    del UnparserTestCase

if __name__ == '__main__':
    unittest.main()

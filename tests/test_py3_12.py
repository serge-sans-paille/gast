import unittest

import ast
import gast
import sys

if sys.version_info >= (3, 13):
    def dump(node):
        return gast.dump(node, show_empty=True)
else:
    def dump(node):
        return gast.dump(node)


class Python3_12TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None

    def test_type_alias(self):
        code = "type Point = tuple[float, float]"
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[TypeAlias(name=Name(id='Point', ctx=Store(),"
                " annotation=None, type_comment=None), type_params=[], "
                "value=Subscript(value=Name(id='tuple', ctx=Load(), "
                "annotation=None, type_comment=None), slice=Tuple(elts=["
                "Name(id='float', ctx=Load(), annotation=None, "
                "type_comment=None), Name(id='float', ctx=Load(), "
                "annotation=None, type_comment=None)], ctx=Load()), "
                "ctx=Load()))], type_ignores=[])")
        self.assertEqual(dump(tree), norm)

    def test_generic_type_alias(self):
        code = "type Point[T] = tuple[T, float]"
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[TypeAlias(name=Name(id='Point', ctx=Store(), "
                "annotation=None, type_comment=None), type_params=[TypeVar("
                "name='T', bound=None)], value=Subscript(value=Name(id='tuple'"
                ", ctx=Load(), annotation=None, type_comment=None), "
                "slice=Tuple(elts=[Name(id='T', ctx=Load(), annotation=None, "
                "type_comment=None), Name(id='float', ctx=Load(), "
                "annotation=None, type_comment=None)], ctx=Load()), ctx=Load()"
                "))], type_ignores=[])")
        self.assertEqual(dump(tree), norm)

    def test_generic_function(self):
        code = "def foo[T]():..."
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=[], "
                "posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[], "
                "kwarg=None, defaults=[]), body=[Expr(value=Constant(value="
                "Ellipsis, kind=None))], decorator_list=[], returns=None, "
                "type_comment=None, type_params=[TypeVar(name='T', "
                "bound=None)])], type_ignores=[])")
        self.assertEqual(dump(tree), norm)

    def test_generic_class(self):
        code = "class foo[T]:..."
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[ClassDef(name='foo', bases=[], keywords=[], "
                "body=[Expr(value=Constant(value=Ellipsis, kind=None))], "
                "decorator_list=[], type_params=[TypeVar(name='T', bound=None)"
                "])], type_ignores=[])")
        self.assertEqual(dump(tree), norm)

if sys.version_info < (3, 12):
    del Python3_12TestCase

if __name__ == '__main__':
    unittest.main()

import unittest

import gast
import sys


class CompatTestCase(unittest.TestCase):

    if sys.version_info.major == 2:

        def test_FunctionDef(self):
            code = 'def foo((x, y)): return x, y'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')
            norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args="
                    "[Tuple(elts=[Name(id='x', ctx=Store(), annotation=None, "
                    "type_comment=None), Name(id='y', ctx=Store(), "
                    "annotation=None, type_comment=None)], ctx=Store())], "
                    "posonlyargs=[], vararg=None, "
                    "kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), "
                    "body=[Return(value=Tuple(elts=[Name(id='x', ctx=Load(), "
                    "annotation=None, type_comment=None), "
                    "Name(id='y', ctx=Load(), "
                    "annotation=None, type_comment=None"
                    ")], ctx=Load()))], decorator_list="
                    "[], returns=None, type_comment=None)], type_ignores=[])")
            self.assertEqual(gast.dump(tree), norm)

    else:

        def test_ArgAnnotation(self):
            code = 'def foo(x:int): pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')
            norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args="
                    "[Name(id='x', ctx=Param(), annotation=Name"
                    "(id='int', ctx=Load(), annotation=None, type_comment=None"
                    "), type_comment=None)], posonlyargs="
                    "[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg="
                    "None, defaults=[]), body=[Pass()], decorator_list=[], "
                    "returns=None, type_comment=None)], type_ignores=[])")
            self.assertEqual(gast.dump(tree), norm)

        def test_KeywordOnlyArgument(self):
            code = 'def foo(*, x=1): pass'
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')
            norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args="
                    "[], posonlyargs=[], vararg=None, kwonlyargs=[Name"
                    "(id='x', ctx=Param(), annotation=None, type_comment=None"
                    ")], kw_defaults=[Constant(value=1, kind=None)], kwarg="
                    "None, defaults=[]), body=[Pass()], decorator_list=[], "
                    "returns=None, type_comment=None)], type_ignores=[])")
            self.assertEqual(gast.dump(tree), norm)

        if sys.version_info.minor >= 6:

            def test_FormattedValue(self):
                code = 'e = 1; f"{e}"'
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')
                norm = ("Module(body=[Assign(targets=[Name(id='e', ctx=Store()"
                        ", annotation=None, type_comment=None"
                        ")], value=Constant(value=1, kind=None), "
                        "type_comment=None), Expr(value="
                        "JoinedStr(values=[FormattedValue(value=Name(id='e', "
                        "ctx=Load(), annotation=None, type_comment=None), "
                        "conversion=-1, format_spec=None)]))], "
                        "type_ignores=[])")
                self.assertEqual(gast.dump(tree), norm)

            def test_JoinedStr(self):
                code = 'e = 1; f"e = {e}"'
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')
                norm = ("Module(body=[Assign(targets=[Name(id='e', ctx=Store()"
                        ", annotation=None, type_comment=None"
                        ")], value=Constant(value=1, kind=None), "
                        "type_comment=None), Expr(value="
                        "JoinedStr(values=[Constant(value='e = ', kind=None), "
                        "FormattedValue(value=Name(id='e', ctx=Load(), "
                        "annotation=None, type_comment=None), "
                        "conversion=-1, format_spec=None)]))], "
                        "type_ignores=[])")
                self.assertEqual(gast.dump(tree), norm)

        if sys.version_info.minor >= 8:

            def test_TypeIgnore(self):
                code = 'def foo(): pass  # type: ignore[excuse]'
                tree = gast.parse(code, type_comments=True)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')
                norm = ("Module(body=[FunctionDef(name='foo', args=arguments("
                        "args=[], posonlyargs=[], vararg=None, kwonlyargs=[], "
                        "kw_defaults=[], kwarg=None, defaults=[]), body=["
                        "Pass()], decorator_list=[], returns=None, "
                        "type_comment=None)], type_ignores="
                        "[TypeIgnore(lineno=1, tag='[excuse]')])")
                self.assertEqual(gast.dump(tree), norm)

            def test_PosonlyArgs(self):
                code = 'def foo(a, /, b): pass'
                tree = gast.parse(code, type_comments=True)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')
                norm = ("Module(body=[FunctionDef(name='foo', args=arguments("
                        "args=[Name(id='b', ctx=Param(), annotation=None, "
                        "type_comment=None)], posonlyargs=[Name(id='a', "
                        "ctx=Param(), annotation=None, type_comment=None)], "
                        "vararg=None, kwonlyargs=[], kw_defaults=[], "
                        "kwarg=None, defaults=[]), body=[Pass()], "
                        "decorator_list=[], returns=None, type_comment=None)"
                        "], type_ignores=[])")
                self.assertEqual(gast.dump(tree), norm)

        else:

            def test_Bytes(self):
                code = 'b"0012"'
                tree = gast.parse(code)
                compile(gast.gast_to_ast(tree), '<test>', 'exec')
                norm = ("Module(body=[Expr(value=Constant(value=b'0012', "
                        "kind=None))], type_ignores=[])")
                self.assertEqual(gast.dump(tree), norm)

    # common

    def test_TryExcept(self):
        code = 'try:pass\nexcept e:pass\nelse:pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[Try(body=[Pass()], handlers=[ExceptHandler("
                "type=Name(id='e', ctx=Load(), annotation=None, "
                "type_comment=None), name=None, body=[Pass()])]"
                ", orelse=[Pass()], finalbody=[])], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_TryExceptNamed(self):
        code = 'try:pass\nexcept e as f:pass\nelse:pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[Try(body=[Pass()], handlers=[ExceptHandler("
                "type=Name(id='e', ctx=Load(), annotation=None, "
                "type_comment=None), name=Name(id='f', ctx="
                "Store(), annotation=None, type_comment=None), body=[Pass()])]"
                ", orelse=[Pass()], finalbody=[])], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_Raise(self):
        codes = ('raise Exception',
                 'raise "Exception"',
                 'raise Exception, "err"',
                 'raise Exception("err")',
                 'raise E, V, T',)
        norms = ("Module(body=[Raise(exc=Name(id='Exception', ctx=Load(), "
                 "annotation=None, type_comment=None),"
                 " cause=None)], type_ignores=[])",

                 "Module(body=[Raise(exc=Constant(value='Exception', kind="
                 "None), cause=None)], type_ignores=[])",

                 "Module(body=[Raise(exc=Call(func=Name(id='Exception', "
                 "ctx=Load(), annotation=None, type_comment=None), "
                 "args=[Constant(value='err', kind=None)], "
                 "keywords=[]), cause=None)], type_ignores=[])",

                 "Module(body=[Raise(exc=Call(func=Name(id='Exception', "
                 "ctx=Load(), annotation=None, type_comment=None), "
                 "args=[Constant(value='err', kind=None)], "
                 "keywords=[]), cause=None)], type_ignores=[])",

                 "Module(body=[Raise(exc=Call(func=Attribute(value=Call("
                 "func=Name(id='E', ctx=Load(), annotation=None, "
                 "type_comment=None), args=[Name(id='V', ctx="
                 "Load(), annotation=None, type_comment=None)], keywords=[]), "
                 "attr='with_traceback', ctx=Load"
                 "()), args=[Name(id='T', ctx=Load(), annotation=None, "
                 "type_comment=None)], keywords=[]), "
                 "cause=None)], type_ignores=[])",)

        if sys.version_info.major == 3:
            codes = codes[0], codes[1], codes[3]
            norms = norms[0], norms[1], norms[3]

        for code, norm in zip(codes, norms):
            tree = gast.parse(code)
            compile(gast.gast_to_ast(tree), '<test>', 'exec')
            self.assertEqual(gast.dump(tree), norm)

    def test_Call(self):
        self.maxDiff = None
        code = 'foo(x, y=1, *args, **kwargs)'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[Expr(value=Call(func=Name(id='foo', ctx=Load"
                "(), annotation=None, type_comment=None"
                "), args=[Name(id='x', ctx=Load(), "
                "annotation=None, type_comment=None), Starred(value=Name("
                "id='args', ctx=Load(), annotation=None, type_comment=None)"
                ", ctx=Load())], keywords=[keyword("
                "arg='y', value=Constant(value=1, kind=None)), keyword(arg"
                "=None, value=Name(id='kwargs', ctx=Load(), annotation=None, "
                "type_comment=None))]))], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_With(self):
        code = 'with open("any"): pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[With(items=[withitem(context_expr=Call(func="
                "Name(id='open', ctx=Load(), annotation=None, "
                "type_comment=None), args=[Constant(value='any', "
                "kind=None)], keywords=[]), optional_vars=None)], body=["
                "Pass()], type_comment=None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_TryFinally(self):
        code = 'try:pass\nfinally:pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[Try(body=[Pass()], handlers=[], orelse=[], "
                "finalbody=[Pass()])], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_star_argument(self):
        code = 'def foo(*a): pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=[], "
                "posonlyargs=[], vararg=Name(id='a', ctx=Param(), "
                "annotation=None, type_comment=None), "
                "kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), "
                "body=[Pass()], decorator_list=[], returns=None, "
                "type_comment=None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_keyword_argument(self):
        code = 'def foo(**a): pass'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=[], "
                "posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[], "
                "kwarg=Name(id='a', ctx=Param(), annotation=None, "
                "type_comment=None), defaults=[]), body=[Pass()], "
                "decorator_list=[], returns=None, type_comment=None)], "
                "type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_Index(self):
        code = 'def foo(a): a[1]'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=["
                "Name(id='a', ctx=Param(), annotation=None, type_comment=None)"
                "], posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[]"
                ", kwarg=None, defaults=[]), body=[Expr(value=Subscript(value="
                "Name(id='a', ctx=Load(), annotation=None, type_comment=None)"
                ", slice=Constant(value=1, kind=None), ctx=Load()"
                "))], decorator_list=[], returns=None, type_comment=None)]"
                ", type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_ExtSlice(self):
        self.maxDiff = None
        code = 'def foo(a): a[:,:]'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=["
                "Name(id='a', ctx=Param(), annotation=None, type_comment=None)"
                "], posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[]"
                ", kwarg=None, defaults=[]), body=[Expr(value=Subscript(value="
                "Name(id='a', ctx=Load(), annotation=None, type_comment=None)"
                ", slice=Tuple(elts=[Slice(lower=None, upper=None, step="
                "None), Slice(lower=None, upper=None, step=None)], ctx=Load())"
                ", ctx=Load()))], decorator_list=[], returns=None, "
                "type_comment=None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_ExtSlices(self):
        self.maxDiff = None
        code = 'def foo(a): a[1,:]'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=["
                "Name(id='a', ctx=Param(), annotation=None, type_comment=None)"
                "], posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[]"
                ", kwarg=None, defaults=[]), body=[Expr(value=Subscript(value="
                "Name(id='a', ctx=Load(), annotation=None, type_comment=None)"
                ", slice=Tuple(elts=[Constant(value=1, kind="
                "None), Slice(lower=None, upper=None, step=None)], ctx=Load())"
                ", ctx=Load()))], decorator_list=[], returns=None, "
                "type_comment=None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_Ellipsis(self):
        self.maxDiff = None
        code = 'def foo(a): a[...]'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=["
                "Name(id='a', ctx=Param(), annotation=None, type_comment=None)"
                "], posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[]"
                ", kwarg=None, defaults=[]), body=[Expr(value=Subscript(value="
                "Name(id='a', ctx=Load(), annotation=None, type_comment=None)"
                ", slice=Constant(value=Ellipsis, kind=None), ctx=Load()))], "
                "decorator_list=[], returns=None, type_comment="
                "None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)

    def test_ExtSliceEllipsis(self):
        self.maxDiff = None
        code = 'def foo(a): a[1, ...]'
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = ("Module(body=[FunctionDef(name='foo', args=arguments(args=["
                "Name(id='a', ctx=Param(), annotation=None, type_comment=None)"
                "], posonlyargs=[], vararg=None, kwonlyargs=[], kw_defaults=[]"
                ", kwarg=None, defaults=[]), body=[Expr(value=Subscript(value="
                "Name(id='a', ctx=Load(), annotation=None, type_comment=None)"
                ", slice=Tuple(elts=[Constant(value=1, kind=None)"
                ", Constant(value=Ellipsis, kind=None)], ctx=Load()), ctx="
                "Load()))], decorator_list=[], returns=None, type_comment="
                "None)], type_ignores=[])")
        self.assertEqual(gast.dump(tree), norm)


if __name__ == '__main__':
    unittest.main()

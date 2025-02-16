import unittest

import ast
import gast
import sys


def dump(node):
    return gast.dump(node, show_empty=True)


class APITestCase(unittest.TestCase):

    def test_literal_eval_string(self):
        code = "1, 3"
        self.assertEqual(ast.literal_eval(code),
                         gast.literal_eval(code))

    def test_literal_eval_code(self):
        code = "[1, 3]"
        tree = ast.parse(code, mode='eval')
        gtree = gast.parse(code, mode='eval')
        self.assertEqual(ast.literal_eval(tree),
                         gast.literal_eval(gtree))

    def test_parse(self):
        code = '''
def foo(x=1, *args, **kwargs):
    return x + y +len(args) + len(kwargs)
        '''
        gast.parse(code)

    def test_unparse(self):
        code = 'def foo(x=1): return x'
        self.assertEqual(gast.unparse(gast.parse(code)),
                         'def foo(x=1):\n    return x')

    def test_dump(self):
        code = 'lambda x: x'
        tree = gast.parse(code, mode='eval')
        zdump = dump(tree)
        norm = ("Expression(body=Lambda(args=arguments(args=[Name("
                "id='x', ctx=Param(), "
                "annotation=None, type_comment=None)], posonlyargs=[], "
                "vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, "
                "defaults=[]), body=Name(id='x', ctx=Load(), "
                "annotation=None, type_comment=None)"
                "))")
        self.assertEqual(zdump, norm)

    def test_walk(self):
        code = 'x + 1'
        tree = gast.parse(code, mode='eval')
        zdump = dump(tree)
        norm = ("Expression(body=BinOp(left=Name(id='x', ctx=Load(), "
                "annotation=None, type_comment=None), op=Add(), "
                "right=Constant(value=1, kind=None)))")
        self.assertEqual(zdump, norm)
        self.assertEqual(len(list(gast.walk(tree))), 6)

    def test_iter_fields(self):
        tree = gast.Constant(value=1, kind=None)
        self.assertEqual({name for name, _ in gast.iter_fields(tree)},
                         {'value', 'kind'})

    def test_iter_child_nodes(self):
        tree = gast.UnaryOp(gast.USub(), gast.Constant(value=1, kind=None))
        self.assertEqual(len(list(gast.iter_fields(tree))),
                         2)

    def test_increment_lineno(self):
        tree = gast.Constant(value=1, kind=None)
        tree.lineno = 1
        gast.increment_lineno(tree)
        self.assertEqual(tree.lineno, 2)

    def test_get_source_segment(self):
        code = 'x + 1'
        tree = gast.parse(code)
        source = gast.get_source_segment(code, tree.body[0].value.left)
        if sys.version_info >= (3, 8):
            self.assertEqual(source, 'x')
        else:
            self.assertEqual(source, None)


    def test_get_source_segment_padded(self):
        code = 'if 1:\n if 2:\n  3'
        tree = gast.parse(code)
        if_tree = tree.body[0].body[0]
        source_nopadding = gast.get_source_segment(code, if_tree, padded=False)
        if sys.version_info >= (3, 8):
            self.assertEqual(source_nopadding, 'if 2:\n  3')
        else:
            self.assertEqual(source_nopadding, None)
        source_padding = gast.get_source_segment(code, if_tree, padded=True)
        if sys.version_info >= (3, 8):
            self.assertEqual(source_padding, ' if 2:\n  3')
        else:
            self.assertEqual(source_padding, None)

    def test_get_docstring_function(self):
        code = 'def foo(): "foo"'
        tree = gast.parse(code)
        func = tree.body[0]
        docs = gast.get_docstring(func)
        self.assertEqual(docs, "foo")

    if sys.version_info >= (3, 5):
        def test_get_docstring_asyncfunction(self):
            code = 'async def foo(): "foo"'
            tree = gast.parse(code)
            func = tree.body[0]
            docs = gast.get_docstring(func)
            self.assertEqual(docs, "foo")

    def test_get_docstring_module(self):
        code = '"foo"'
        tree = gast.parse(code)
        docs = gast.get_docstring(tree)
        self.assertEqual(docs, "foo")

    def test_get_docstring_class(self):
        code = 'class foo: "foo"'
        tree = gast.parse(code)
        cls = tree.body[0]
        docs = gast.get_docstring(cls)
        self.assertEqual(docs, "foo")

    def test_get_docstring_expr(self):
        code = '1'
        tree = gast.parse(code)
        func = tree
        docs = gast.get_docstring(func)
        self.assertEqual(docs, None)

    def test_copy_location(self):
        tree = gast.Constant(value=1, kind=None)
        tree.lineno = 1
        tree.col_offset = 2

        node = gast.Constant(value=2, kind=None)
        gast.copy_location(node, tree)
        self.assertEqual(node.lineno, tree.lineno)
        self.assertEqual(node.col_offset, tree.col_offset)

    def test_fix_missing_locations(self):
        node = gast.Constant(value=6, kind=None)
        tree = gast.UnaryOp(gast.USub(), node)
        tree.lineno = 1
        tree.col_offset = 2
        gast.fix_missing_locations(tree)
        self.assertEqual(node.lineno, tree.lineno)
        self.assertEqual(node.col_offset, tree.col_offset)

    def test_NodeTransformer(self):
        node = gast.Constant(value=6, kind=None)
        tree = gast.UnaryOp(gast.USub(), node)

        class Trans(gast.NodeTransformer):

            def visit_Constant(self, node):
                node.value *= 2
                return node

        tree = Trans().visit(tree)

        self.assertEqual(node.value, 12)

    def test_NodeVisitor(self):
        node = gast.Constant(value=6, kind=None)
        tree = gast.UnaryOp(gast.USub(), node)

        class Vis(gast.NodeTransformer):

            def __init__(self):
                self.state = []

            def visit_Constant(self, node):
                self.state.append(node.value)

        vis = Vis()
        vis.visit(tree)

        self.assertEqual(vis.state, [6])

    def test_NodeConstructor(self):
        node0 = gast.Name()
        load = gast.Load()
        node1 = gast.Name('id', load, None, None)
        node2 = gast.Name('id', load, None, type_comment=None)
        with self.assertRaises(TypeError):
            node1 = gast.Name('id', 'ctx', 'annotation', 'type_comment',
                              'random_field')
        for field in gast.Name._fields:
            self.assertEqual(getattr(node1, field), getattr(node2, field))


if __name__ == '__main__':
    unittest.main()

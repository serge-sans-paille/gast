import unittest

import ast
import gast
import sys


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
                         ast.literal_eval(tree))

    def test_parse(self):
        code = '''
def foo(x=1, *args, **kwargs):
    return x + y +len(args) + len(kwargs)
        '''
        tree = gast.parse(code)

    def test_dump(self):
        code = 'lambda x: x'
        tree = gast.parse(code, mode='eval')
        dump = gast.dump(tree)
        norm = ("Expression(body=Lambda(args=arguments(args=[Name(id='x', "
                "ctx=Param(), annotation=None)], vararg=None, kwonlyargs=[], "
                "kw_defaults=[], kwarg=None, defaults=[]), body=Name(id='x', "
                "ctx=Load(), annotation=None)))")
        self.assertEqual(dump, norm)

    def test_walk(self):
        code = 'x + 1'
        tree = gast.parse(code, mode='eval')
        dump = gast.dump(tree)
        norm = ("Expression(body=BinOp(left=Name(id='x', ctx=Load(), "
                "annotation=None), op=Add(), right=Num(n=1)))")
        self.assertEqual(dump, norm)
        self.assertEqual(len(list(gast.walk(tree))), 6)

    def test_iter_fields(self):
        tree = gast.Num(n=1)
        self.assertEqual({name for name, _ in gast.iter_fields(tree)},
                         {'n'})

    def test_iter_child_nodes(self):
        tree = gast.UnaryOp(gast.USub(), gast.Num(n=1))
        self.assertEqual(len(list(gast.iter_fields(tree))),
                         2)

    def test_increment_lineno(self):
        tree = gast.Num(n=1)
        tree.lineno = 1
        gast.increment_lineno(tree)
        self.assertEqual(tree.lineno, 2)

    def test_get_docstring(self):
        code = 'def foo(): "foo"'
        tree = gast.parse(code)
        func = tree.body[0]
        docs = gast.get_docstring(func)
        self.assertEqual(docs, "foo")

    def test_copy_location(self):
        tree = gast.Num(n=1)
        tree.lineno = 1
        tree.col_offset = 2

        node = gast.Num(n=2)
        gast.copy_location(node, tree)
        self.assertEqual(node.lineno, tree.lineno)
        self.assertEqual(node.col_offset, tree.col_offset)

    def test_fix_missing_locations(self):
        node = gast.Num(n=6)
        tree = gast.UnaryOp(gast.USub(), node)
        tree.lineno = 1
        tree.col_offset = 2
        gast.fix_missing_locations(tree)
        self.assertEqual(node.lineno, tree.lineno)
        self.assertEqual(node.col_offset, tree.col_offset)

    def test_NodeTransformer(self):
        node = gast.Num(n=6)
        tree = gast.UnaryOp(gast.USub(), node)

        class Trans(gast.NodeTransformer):

            def visit_Num(self, node):
                node.n *= 2
                return node

        tree = Trans().visit(tree)

        self.assertEqual(node.n, 12)

    def test_NodeVisitor(self):
        node = gast.Num(n=6)
        tree = gast.UnaryOp(gast.USub(), node)

        class Vis(gast.NodeTransformer):

            def __init__(self):
                self.state = []

            def visit_Num(self, node):
                self.state.append(node.n)

        vis = Vis()
        vis.visit(tree)

        self.assertEqual(vis.state, [6])


if __name__ == '__main__':
    unittest.main()

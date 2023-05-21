import unittest

import sys
import ast
import gast

class NoCorespondance(Exception):
    def __init__(self, node):
        self.node = node

class CheckAllNodesInMapping(gast.NodeVisitor):
    def __init__(self, mapping) -> None:
        self.mapping = mapping
    
    def visit(self, node):
        newname = node.__class__.__name__
        
        if newname in ('Param', 'Store', 'Load', 'Del', 'AugLoad', 'AugStore'):
            # expr_context nodes never have a corespondance. 
            assert node not in self.mapping
        else:
            
            try:
                oldname = self.mapping[node].__class__.__name__
            except KeyError as e:
                raise NoCorespondance(node) from e
            
            if oldname == 'arg':
                assert newname == 'Name'
                assert node in self.mapping
            else:
                assert oldname == newname
                assert node in self.mapping
        
        self.generic_visit(node)


class APITestCase(unittest.TestCase):

    def test_simple_mapping(self):
        code = "1, 3"
        gnode, mapping = gast.parse_and_map(code)
        assert isinstance(mapping[gnode], ast.Module)
        CheckAllNodesInMapping(mapping).visit(gnode)
    
    def test_simple_FunctionDef(self):
        code = 'def foo(x, y): return x, y'
        gnode, mapping = gast.parse_and_map(code)
        CheckAllNodesInMapping(mapping).visit(gnode)
    
    if sys.version_info.major==3:

        def test_OnlyPython3CornerCase(self):
            code = 'try: {}[1]\nexcept KeyError as e:\n ...'
            gnode, mapping = gast.parse_and_map(code)
            store_name = next(n for n in gast.walk(gnode) if isinstance(n, gast.Name) and isinstance(n.ctx, gast.Store))
            try:
                CheckAllNodesInMapping(mapping).visit(gnode)
            except NoCorespondance as e:
                assert e.node == store_name
        
        def test_ArgAnnotation(self):
            code = 'def foo(x:int): pass'
            gnode, mapping = gast.parse_and_map(code)
            CheckAllNodesInMapping(mapping).visit(gnode)
        
        def test_KeywordOnlyArgument(self):
            code = 'def foo(*, x=1): pass'
            gnode, mapping = gast.parse_and_map(code)
            CheckAllNodesInMapping(mapping).visit(gnode)

        if sys.version_info.minor >= 6:
            def test_FormattedValue(self):
                code = 'e = 1; f"{e}"'
                gnode, mapping = gast.parse_and_map(code)
                CheckAllNodesInMapping(mapping).visit(gnode)
        
        if sys.version_info.minor >= 8:

            def test_TypeIgnore(self):
                code = 'def foo(): pass  # type: ignore[excuse]'
                gnode, mapping = gast.parse_and_map(code)
                CheckAllNodesInMapping(mapping).visit(gnode)
            
            def test_PosonlyArgs(self):
                code = 'def foo(a, /, b): pass'
                gnode, mapping = gast.parse_and_map(code)
                CheckAllNodesInMapping(mapping).visit(gnode)

import ast as _ast
import sys

if sys.version_info.major==3:
    from .ast3 import Ast3ToGAst as AstToGAst
if sys.version_info.major==2:
    from .ast2 import Ast2ToGAst as AstToGAst

class MapAstToGAst(AstToGAst):
    def __init__(self) -> None:
        self.mapping = {}
    def visit(self, node):
        newnode = super().visit(node)
        if not isinstance(node, _ast.expr_context):
            self.mapping[newnode] = node
        return newnode

def parse_and_map(*args, **kwargs):
    # returns a tuple: (gast node, mapping from gast node to ast node)
    astnode = _ast.parse(*args, **kwargs)
    mapvisitor = MapAstToGAst()
    newnode = mapvisitor.visit(astnode)
    return newnode, mapvisitor.mapping

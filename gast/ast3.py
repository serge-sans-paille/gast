from gast.astn import AstToGAst, GAstToAst
import gast
import ast
import sys


class Ast3ToGAst(AstToGAst):

    def visit_Name(self, node):
        new_node = gast.Name(
            self._visit(node.id),
            self._visit(node.ctx),
            None,
        )
        return ast.copy_location(new_node, node)

    def visit_arg(self, node):
        new_node = gast.Name(
            self._visit(node.arg),
            gast.Param(),
            self._visit(node.annotation),
        )
        return ast.copy_location(new_node, node)

    if 2 <= sys.version_info.minor <= 3:

        def _make_annotated_arg(self, parent, identifier, annotation):
            if identifier is None:
                return None
            new_node = gast.Name(
                self._visit(identifier),
                gast.Param(),
                self._visit(annotation),
            )
            return ast.copy_location(new_node, parent)

        def visit_arguments(self, node):
            new_node = gast.arguments(
                [self._visit(n) for n in node.args],
                self._make_annotated_arg(node,
                                         node.vararg,
                                         self._visit(node.varargannotation)),
                [self._visit(n) for n in node.kwonlyargs],
                self._visit(node.kw_defaults),
                self._make_annotated_arg(node,
                                         node.kwarg,
                                         self._visit(node.kwargannotation)),
                self._visit(node.defaults),
            )
            return new_node


class GAstToAst3(GAstToAst):

    def _make_arg(self, node):
        if node is None:
            return None
        new_node = ast.arg(
            self._visit(node.id),
            self._visit(node.annotation),
        )
        return ast.copy_location(new_node, node)

    def visit_Name(self, node):
        new_node = ast.Name(
            self._visit(node.id),
            self._visit(node.ctx),
        )
        return ast.copy_location(new_node, node)

    if 2 <= sys.version_info.minor <= 3:

        def visit_arguments(self, node):
            if node.vararg is None:
                vararg = None
                varargannotation = None
            else:
                vararg = node.vararg.id
                varargannotation = self._visit(node.vararg.annotation)
            if node.kwarg is None:
                kwarg = None
                kwargannotation = None
            else:
                kwarg = node.kwarg.id
                kwargannotation = self._visit(node.kwarg.annotation)

            new_node = ast.arguments(
                [self._make_arg(n) for n in node.args],
                vararg, varargannotation,
                [self._make_arg(n) for n in node.kwonlyargs],
                kwarg, kwargannotation,
                self._visit(node.defaults),
                self._visit(node.kw_defaults),
            )
            return new_node
    else:
        def visit_arguments(self, node):
            new_node = ast.arguments(
                [self._make_arg(n) for n in node.args],
                self._make_arg(node.vararg),
                [self._make_arg(n) for n in node.kwonlyargs],
                self._visit(node.kw_defaults),
                self._make_arg(node.kwarg),
                self._visit(node.defaults),
            )
            return new_node


def ast_to_gast(node):
    return Ast3ToGAst().visit(node)


def gast_to_ast(node):
    return GAstToAst3().visit(node)

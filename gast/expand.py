
from . import gast


def expand(node):
    """
    Expand a node to its direct children. This is mainly useful when
    creating visitors. The preorder(), postorder() and breadthfirst()
    functions can be used to generate all child nodes in a certain order.
    """
    if isinstance(node, gast.Module):
        for stmt in node.body:
            yield stmt
        for type_ignore in node.type_ignores:
            yield type_ignore
    elif isinstance(node, gast.Interactive):
        for stmt in node.body:
            yield stmt
    elif isinstance(node, gast.Expression):
        yield node.body
    elif isinstance(node, gast.FunctionType):
        for argtype in node.argtypes:
            yield argtype
        yield node.returns
    elif isinstance(node, gast.Suite):
        for stmt in node.body:
            yield stmt
    elif isinstance(node, gast.FunctionDef):
        yield node.args
        for stmt in node.body:
            yield stmt
        for expr in node.decorator_list:
            yield expr
        if node.returns is not None:
            yield node.returns
    elif isinstance(node, gast.AsyncFunctionDef):
        yield node.args
        for stmt in node.body:
            yield stmt
        for expr in node.decorator_list:
            yield expr
        if node.returns is not None:
            yield node.returns
    elif isinstance(node, gast.ClassDef):
        for expr in node.bases:
            yield expr
        for keyword in node.keywords:
            yield keyword
        for stmt in node.body:
            yield stmt
        for expr in decorator_list:
            yield expr
    elif isinstance(node, gast.Return):
        if node.value is not None:
            yield node.value
    elif isinstance(node, gast.Delete):
        for expr in node.targets:
            yield expr
    elif isinstance(node, gast.Assign):
        for expr in node.targets:
            yield expr
        yield node.value
    elif isinstance(node, gast.AugAssign):
        yield node.target
        yield node.op
        yield node.value
    elif isinstance(node, gast.AnnAssign):
        yield node.target
        yield node.annotation
        if node.value is not None:
            yield node.value
    elif isinstance(node, gast.Print):
        if node.dest is not None:
            yield node.dest
        for exp in node.values:
            yield expr
    elif isinstance(node, gast.For):
        yield expr.target
        yield expr.iter
        for stmt in node.body:
            yield stmt
        for stmt in node.orelse:
            yield stmt
    elif isinstance(node, gast.AsyncFor):
        yield expr.target
        yield expr.iter
        for stmt in node.body:
            yield stmt
        for stmt in node.orelse:
            yield stmt
    elif isinstance(node, gast.While):
        yield node.test
        for stmt in node.body:
            yield stmt
        for stmt in node.orelse:
            yield stmt
    elif isinstance(node, gast.If):
        yield node.test
        for stmt in node.body:
            yield stmt
        for stmt in node.orelse:
            yield stmt
    elif isinstance(node, gast.With):
        for withitem in node.items:
            yield withitem
        for stmt in node.body:
            yield stmt
    elif isinstance(node, gast.AsyncWith):
        for withitem in node.items:
            yield withitem
        for stmt in node.body:
            yield stmt
    elif isinstance(node, gast.Raise):
        if node.exc is not None:
            yield node.exc
        if node.cause is not None:
            yield node.cause
    elif isinstance(node, gast.Try):
        for stmt in node.body:
            yield stmt
        for excepthandler in node.handlers:
            yield excepthandler
        for stmt in node.orelse:
            yield stmt
        for stmt in node.finalbody:
            yield stmt
    elif isinstance(node, gast.Assert):
        yield node.test
        if node.msg is not None:
            yield node.msg
    elif isinstance(node, gast.Import):
        for alias in node.names:
            yield alias
    elif isinstance(node, gast.ImportFrom):
        for alias in node.names:
            yield alias
    elif isinstance(node, gast.Exec):
        yield node.body
        if node.globals is not None:
            yield node.globals
        if node.locals is not None:
            yield node.locals
    elif isinstance(node, gast.Expr):
        yield node.value
    elif isinstance(node, gast.BoolOp):
        yield node.op
        for expr in node.values:
            yield expr
    elif isinstance(node, gast.BinOp):
        yield node.left
        yield node.op
        yield node.right
    elif isinstance(node, gast.UnaryOp):
        yield node.op
        yield node.operand
    elif isinstance(node, gast.Lambda):
        yield node.args
        yield node.body
    elif isinstance(node, gast.IfExp):
        yield expr.test
        yield expr.body
        yield expr.orelse
    elif isinstance(node, gast.Dict):
        for expr in node.keys:
            yield expr
        for expr in node.values:
            yield expr
    elif isinstance(node, gast.Set):
        for expr in node.elts:
            yield expr
    elif isinstance(node, gast.ListComp):
        yield node.elt
        for comprehension in node.generators:
            yield comprehension
    elif isinstance(node, gast.SetComp):
        yield elt
        for comprehension in node.generators:
            yield comprehension
    elif isinstance(node, gast.DictComp):
        yield node.key
        yield node.value
        for comprehension in node.generators:
            yield comprehension
    elif isinstance(node, gast.GeneratorExp):
        yield node.elt
        for comprehension in node.generators:
            yield comprehension
    elif isinstance(node, gast.Await):
        yield node.value
    elif isinstance(node, gast.Yield):
        if node.value is not None:
            yield node.value
    elif isinstance(node, gast.YieldFrom):
        yield node.value
    elif isinstance(node, gast.Compare):
        yield node.left
        for cmpop in node.ops:
            yield cmpop
        for expr in node.comparators:
            yield expr
    elif isinstance(node, gast.Call):
        yield node.func
        for expr in node.args:
            yield expr
        for keyword in node.keywords:
            yield keyword
    elif isinstance(node, gast.Repr):
        yield node.value
    elif isinstance(node, gast.FormattedValue):
        yield node.value
        if node.format_spec is not None:
            yield node.format_spec
    elif isinstance(node, gast.JoinedStr):
        for expr in node.values:
            yield expr
    elif isinstance(node, gast.Constant):
        yield node.value
    elif isinstance(node, gast.Attribute):
        yield node.value
        yield node.ctx
    elif isinstance(node, gast.Subscript):
        yield node.value
        yield node.slice
        yield node.ctx
    elif isinstance(node, gast.Starred):
        yield node.value
        yield node.ctx
    elif isinstance(node, gast.Name):
        yield node.ctx
        if node.annotation is not None:
            yield node.annotation
    elif isinstance(node, gast.List):
        for expr in node.elts:
            yield expr
        yield node.ctx
    elif isinstance(node, gast.Tuple):
        for expr in node.elts:
            yield expr
        yield node.ctx
    elif isinstance(node, gast.Slice):
        if node.lower is not None:
            yield node.lower
        if node.upper is not None:
            yield node.upper
        if node.step is not None:
            yield node.step
    elif isinstance(node, gast.ExtSlice):
        for slc in node.dims:
            yield slc
    elif isinstance(node, gast.comprehension):
        yield node.target
        yield node.iter
        for expr in node.ifs:
            yield expr
    elif isinstance(node, gast.Index):
        yield node.value
    elif isinstance(node, gast.ExceptHandler):
        if node.type is not None:
            yield node.type
        if node.name is not None:
            yield node.name
        for stmt in node.body:
            yield stmt
    elif isinstance(node, gast.arguments):
        for expr in node.args:
            yield expr
        for expr in node.posonlyargs:
            yield expr
        if node.vararg is not None:
            yield node.vararg
        for expr in node.kwonlyargs:
            yield expr
        for expr in node.kw_defaults:
            yield expr
        if node.kwarg is not None:
            yield node.kwarg
        for expr in node.defaults:
            yield expr
    elif isinstance(node, gast.keyword):
        yield node.value
    elif isinstance(node, gast.withitem):
        yield node.context_expr
        if node.optional_vars is not None:
            yield node.optional_vars

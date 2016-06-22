import sys as _sys
from _ast import AST
import ast as _ast


def _make_node(Name, Fields, Attributes):
    def create_node(self, *args, **kwargs):
        nbparam = len(args) + len(kwargs)
        assert nbparam in (0, len(Fields)), \
            "Bad argument number for {}: {}, expecting {}".\
            format(Name, nbparam, len(Fields))
        self._fields = Fields
        self._attributes = Attributes
        for argname, argval in zip(self._fields, args):
            setattr(self, argname, argval)
        for argname, argval in kwargs.items():
            assert argname in Fields, \
                    "Invalid Keyword argument for {}: {}".format(Name, argname)
            setattr(self, argname, argval)

    setattr(_sys.modules[__name__],
            Name,
            type(Name,
                 (AST,),
                 {'__init__': create_node}))

_nodes = {
    # mod
    'Module': (('body',), ()),
    'Interactive': (('body',), ()),
    'Expression': (('body',), ()),
    'Suite': (('body',), ()),

    # stmt
    'FunctionDef': (('name', 'args', 'body', 'decorator_list', 'returns',),
                    ('lineno', 'col_offset',)),
    'AsyncFunctionDef': (('name', 'args', 'body',
                          'decorator_list', 'returns',),
                         ('lineno', 'col_offset',)),
    'ClassDef': (('name', 'bases', 'keywords', 'body', 'decorator_list',),
                 ('lineno', 'col_offset',)),
    'Return': (('value',), ('lineno', 'col_offset',)),
    'Delete': (('targets',), ('lineno', 'col_offset',)),
    'Assign': (('targets', 'value',), ('lineno', 'col_offset',)),
    'AugAssign': (('target', 'op', 'value',), ('lineno', 'col_offset',)),
    'Print': (('dest', 'values', 'nl',), ('lineno', 'col_offset',)),
    'For': (('target', 'iter', 'body', 'orelse',), ('lineno', 'col_offset',)),
    'AsyncFor': (('target', 'iter', 'body', 'orelse',),
                 ('lineno', 'col_offset',)),
    'While': (('test', 'body', 'orelse',), ('lineno', 'col_offset',)),
    'If': (('test', 'body', 'orelse',), ('lineno', 'col_offset',)),
    'With': (('items', 'body',), ('lineno', 'col_offset',)),
    'AsyncWith': (('items', 'body',), ('lineno', 'col_offset',)),
    'Raise': (('exc', 'cause',), ('lineno', 'col_offset',)),
    'Try': (('body', 'handlers', 'orelse', 'finalbody',),
            ('lineno', 'col_offset',)),
    'Assert': (('test', 'msg',), ('lineno', 'col_offset',)),
    'Import': (('names',), ('lineno', 'col_offset',)),
    'ImportFrom': (('module', 'names', 'level',), ('lineno', 'col_offset',)),
    'Exec': (('body', 'globals', 'locals',), ('lineno', 'col_offset',)),
    'Global': (('names',), ('lineno', 'col_offset',)),
    'Nonlocal': (('names',), ('lineno', 'col_offset',)),
    'Expr': (('value',), ('lineno', 'col_offset',)),
    'Pass': ((), ('lineno', 'col_offset',)),
    'Break': ((), ('lineno', 'col_offset',)),
    'Continue': ((), ('lineno', 'col_offset',)),

    # expr

    'BoolOp': (('op', 'values',), ('lineno', 'col_offset',)),
    'BinOp': (('left', 'op', 'right',), ('lineno', 'col_offset',)),
    'UnaryOp': (('op', 'operand',), ('lineno', 'col_offset',)),
    'Lambda': (('args', 'body',), ('lineno', 'col_offset',)),
    'IfExp': (('test', 'body', 'orelse',), ('lineno', 'col_offset',)),
    'Dict': (('keys', 'values',), ('lineno', 'col_offset',)),
    'Set': (('elts',), ('lineno', 'col_offset',)),
    'ListComp': (('elt', 'generators',), ('lineno', 'col_offset',)),
    'SetComp': (('elt', 'generators',), ('lineno', 'col_offset',)),
    'DictComp': (('key', 'value', 'generators',), ('lineno', 'col_offset',)),
    'GeneratorExp': (('elt', 'generators',), ('lineno', 'col_offset',)),
    'Await': (('value',), ('lineno', 'col_offset',)),
    'Yield': (('value',), ('lineno', 'col_offset',)),
    'YieldFrom': (('value',), ('lineno', 'col_offset',)),
    'Compare': (('left', 'ops', 'comparators',), ('lineno', 'col_offset',)),
    'Call': (('func', 'args', 'keywords',), ('lineno', 'col_offset',)),
    'Repr': (('value',), ('lineno', 'col_offset',)),
    'Num': (('n',), ('lineno', 'col_offset',)),
    'Str': (('s',), ('lineno', 'col_offset',)),
    'Bytes': (('s',), ('lineno', 'col_offset',)),
    'NameConstant': (('value',), ('lineno', 'col_offset',)),
    'Ellipsis': ((), ('lineno', 'col_offset',)),
    'Attribute': (('value', 'attr', 'ctx',), ('lineno', 'col_offset',)),
    'Subscript': (('value', 'slice', 'ctx',), ('lineno', 'col_offset',)),
    'Starred': (('value', 'ctx',), ('lineno', 'col_offset',)),
    'Name': (('id', 'ctx', 'annotation'), ('lineno', 'col_offset',)),
    'List': (('elts', 'ctx',), ('lineno', 'col_offset',)),
    'Tuple': (('elts', 'ctx',), ('lineno', 'col_offset',)),

    # expr_context
    'Load': ((), ()),
    'Store': ((), ()),
    'Del': ((), ()),
    'AugLoad': ((), ()),
    'AugStore': ((), ()),
    'Param': ((), ()),

    # slice
    'Slice': (('lower', 'upper', 'step'), ()),
    'ExtSlice': (('dims',), ()),
    'Index': (('value',), ()),

    # boolop
    'And': ((), ()),
    'Or': ((), ()),

    # operator
    'Add': ((), ()),
    'Sub': ((), ()),
    'Mult': ((), ()),
    'MatMult': ((), ()),
    'Div': ((), ()),
    'Mod': ((), ()),
    'Pow': ((), ()),
    'LShift': ((), ()),
    'RShift': ((), ()),
    'BitOr': ((), ()),
    'BitXor': ((), ()),
    'BitAnd': ((), ()),
    'FloorDiv': ((), ()),

    # unaryop
    'Invert': ((), ()),
    'Not': ((), ()),
    'UAdd': ((), ()),
    'USub': ((), ()),

    # cmpop
    'Eq': ((), ()),
    'NotEq': ((), ()),
    'Lt': ((), ()),
    'LtE': ((), ()),
    'Gt': ((), ()),
    'GtE': ((), ()),
    'Is': ((), ()),
    'IsNot': ((), ()),
    'In': ((), ()),
    'NotIn': ((), ()),

    # comprehension
    'comprehension': (('target', 'iter', 'ifs'), ()),

    # excepthandler
    'ExceptHandler': (('type', 'name', 'body'), ('lineno', 'col_offset')),

    # arguments
    'arguments': (('args', 'vararg', 'kwonlyargs', 'kw_defaults',
                   'kwarg', 'defaults'), ()),
    # keyword
    'keyword': (('arg', 'value'), ()),

    # alias
    'alias': (('name', 'asname'), ()),

    # withitem
    'withitem': (('context_expr', 'optional_vars'), ()),
}

for node in _nodes.items():
    _make_node(node[0], *node[1])

if _sys.version_info.major == 2:
    from .ast2 import ast_to_gast, gast_to_ast
if _sys.version_info.major == 3:
    from .ast3 import ast_to_gast, gast_to_ast


def parse(*args, **kwargs):
    return ast_to_gast(_ast.parse(*args, **kwargs))


def literal_eval(node_or_string):
    if isinstance(node_or_string, AST):
        node_or_string = gast_to_ast(node_or_string)
    return _ast.literal_eval(node_or_string)


def get_docstring(node, clean=True):
    if not isinstance(node, (FunctionDef, ClassDef, Module)):
        raise TypeError("%r can't have docstrings" % node.__class__.__name__)
    if node.body and isinstance(node.body[0], Expr) and \
       isinstance(node.body[0].value, Str):
        if clean:
            import inspect
            return inspect.cleandoc(node.body[0].value.s)
        return node.body[0].value.s

GAST, daou naer!
================

A generic AST to represent Python2 and Python3's Abstract Syntax Tree(AST).

GAST provides a compatibility layer between the AST of various Python versions,
as produced by ``ast.parse`` from the standard ``ast`` module.

Basic Usage
-----------

.. code:: python

    >>> import ast, gast
    >>> code = open('file.py').read()
    >>> tree = ast.parse(code)
    >>> gtree = gast.ast_to_gast(tree)
    >>> ... # process gtree
    >>> tree = gast.gast_to_ast(gtree)
    >>> ... # do stuff specific to tree

API
---

``gast`` provides the same API as the ``ast`` module. All functions and classes
from the ``ast`` module are also available in the ``gast`` module, and work
accordingly on the ``gast`` tree.

Three notable exceptions:

1. ``gast.parse`` directly produces a GAST node. It's equivalent to running
       ``gast.ast_to_gast`` on the output of ``ast.parse``.

2. ``gast.dump`` dumps the ``gast`` common representation, not the original
       one.

3. ``gast.gast_to_ast`` and ``gast.ast_to_gast`` can be used to convert
       from one ast to the other, back and forth.

Version Compatibility
---------------------

GAST is tested using ``tox`` and Travis on the following Python versions:

- 2.7
- 3.4
- 3.5
- 3.6


AST Changes
-----------


Python3
*******

The AST used by GAST is the same as the one used in Python3.5, with the
notable exception of ``ast.arg`` being replaced by ``ast.Name`` with an
``ast.Param`` context. Additionally, ``ast.Name`` has an extra ``annotation``
field.

Python2
*******

To cope with Python3 features, several nodes from the Python2 AST are extended
with some new attributes/children.

- ``FunctionDef`` nodes have a ``returns`` attribute.

- ``ClassDef`` nodes have a ``keywords`` attribute.

- ``With``'s ``context_expr`` and ``optional_vars`` fields are hold in a
  ``withitem`` object.

- ``Raise``'s ``type``, ``inst`` and ``tback`` fields are hold in a single
  ``exc`` field, using the transformation ``raise E, V, T => raise E(V).with_traceback(T)``.

- ``TryExcept`` and ``TryFinally`` nodes are merged in the ``Try`` node.

- ``Name`` nodes have an ``annotation`` attribute.

- ``arguments`` nodes have a ``kwonlyargs`` and ``kw_defaults`` attributes.

- ``Call`` nodes loose their ``starargs`` attribute, replaced by an
  argument wrapped in a ``Starred`` node. They also loose their ``kwargs``
  attribute, wrapped in a ``keyword`` node with the identifier set to
  ``None``, as done in Python3.

- ``comprehension`` nodes have an ``async`` attribute (that is always set
  to 0).

Pit Falls
*********

- In Python3, ``None``, ``True`` and ``False`` are parsed as ``NamedConstant``
  while they are parsed as regular ``Name`` in Python2. ``gast`` uses the same
  convention.

ASDL
****

.. code::

    -- ASDL's six builtin types are identifier, int, string, bytes, object, singleton

    module Python
    {
        mod = Module(stmt* body)
            | Interactive(stmt* body)
            | Expression(expr body)

            -- not really an actual node but useful in Jython's typesystem.
            | Suite(stmt* body)

        stmt = FunctionDef(identifier name, arguments args,
                           stmt* body, expr* decorator_list, expr? returns)
              | AsyncFunctionDef(identifier name, arguments args,
                                 stmt* body, expr* decorator_list, expr? returns)

              | ClassDef(identifier name,
                 expr* bases,
                 keyword* keywords,
                 stmt* body,
                 expr* decorator_list)
              | Return(expr? value)

              | Delete(expr* targets)
              | Assign(expr* targets, expr value)
              | AugAssign(expr target, operator op, expr value)

              -- not sure if bool is allowed, can always use int
              | Print(expr? dest, expr* values, bool nl)

              -- use 'orelse' because else is a keyword in target languages
              | For(expr target, expr iter, stmt* body, stmt* orelse)
              | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse)
              | While(expr test, stmt* body, stmt* orelse)
              | If(expr test, stmt* body, stmt* orelse)
              | With(withitem* items, stmt* body)
              | AsyncWith(withitem* items, stmt* body)

              | Raise(expr? exc, expr? cause)
              | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
              | Assert(expr test, expr? msg)

              | Import(alias* names)
              | ImportFrom(identifier? module, alias* names, int? level)

              -- Doesn't capture requirement that locals must be
              -- defined if globals is
              -- still supports use as a function!
              | Exec(expr body, expr? globals, expr? locals)

              | Global(identifier* names)
              | Nonlocal(identifier* names)
              | Expr(expr value)
              | Pass | Break | Continue

              -- XXX Jython will be different
              -- col_offset is the byte offset in the utf8 string the parser uses
              attributes (int lineno, int col_offset)

              -- BoolOp() can use left & right?
        expr = BoolOp(boolop op, expr* values)
             | BinOp(expr left, operator op, expr right)
             | UnaryOp(unaryop op, expr operand)
             | Lambda(arguments args, expr body)
             | IfExp(expr test, expr body, expr orelse)
             | Dict(expr* keys, expr* values)
             | Set(expr* elts)
             | ListComp(expr elt, comprehension* generators)
             | SetComp(expr elt, comprehension* generators)
             | DictComp(expr key, expr value, comprehension* generators)
             | GeneratorExp(expr elt, comprehension* generators)
             -- the grammar constrains where yield expressions can occur
             | Await(expr value)
             | Yield(expr? value)
             | YieldFrom(expr value)
             -- need sequences for compare to distinguish between
             -- x < 4 < 3 and (x < 4) < 3
             | Compare(expr left, cmpop* ops, expr* comparators)
             | Call(expr func, expr* args, keyword* keywords)
             | Repr(expr value)
             | Num(object n) -- a number as a PyObject.
             | Str(string s) -- need to specify raw, unicode, etc?
             | FormattedValue(expr value, int? conversion, expr? format_spec)
             | JoinedStr(expr* values)
             | Bytes(bytes s)
             | NameConstant(singleton value)
             | Ellipsis

             -- the following expression can appear in assignment context
             | Attribute(expr value, identifier attr, expr_context ctx)
             | Subscript(expr value, slice slice, expr_context ctx)
             | Starred(expr value, expr_context ctx)
             | Name(identifier id, expr_context ctx, expr? annotation)
             | List(expr* elts, expr_context ctx)
             | Tuple(expr* elts, expr_context ctx)

              -- col_offset is the byte offset in the utf8 string the parser uses
              attributes (int lineno, int col_offset)

        expr_context = Load | Store | Del | AugLoad | AugStore | Param

        slice = Slice(expr? lower, expr? upper, expr? step)
              | ExtSlice(slice* dims)
              | Index(expr value)

        boolop = And | Or

        operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift
                     | RShift | BitOr | BitXor | BitAnd | FloorDiv

        unaryop = Invert | Not | UAdd | USub

        cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

        comprehension = (expr target, expr iter, expr* ifs)

        excepthandler = ExceptHandler(expr? type, expr? name, stmt* body)
                        attributes (int lineno, int col_offset)

        arguments = (expr* args, expr? vararg, expr* kwonlyargs, expr* kw_defaults,
                     expr? kwarg, expr* defaults)

        -- keyword arguments supplied to call (NULL identifier for **kwargs)
        keyword = (identifier? arg, expr value)

        -- import name with optional 'as' alias.
        alias = (identifier name, identifier? asname)

        withitem = (expr context_expr, expr? optional_vars)
    }

import unittest

import ast
import gast
import sys



class Python3_12TestCase(unittest.TestCase):

    def test_type_alias(self):
        self.maxDiff = None
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
        self.assertEqual(gast.dump(tree), norm)

if sys.version_info < (3, 12):
    del Python3_12TestCase

if __name__ == '__main__':
    unittest.main()

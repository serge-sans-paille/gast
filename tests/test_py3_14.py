import unittest

import ast
import gast
import sys

def dump(node):
    return gast.dump(node, show_empty=True)


class Python3_14TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None

    def test_template_string(self):
        code = '''
food = "cheese"
string = f"Tasty {food}!"
template = t"Tasty {food}!"
'''
        tree = gast.parse(code)
        compile(gast.gast_to_ast(tree), '<test>', 'exec')
        norm = (
            "Module(body=["
                "Assign(targets=[Name(id='food', ctx=Store(), annotation=None, type_comment=None)], "
                       "value=Constant(value='cheese', kind=None), type_comment=None), "
                "Assign(targets=[Name(id='string', ctx=Store(), annotation=None, type_comment=None)], "
                       "value=JoinedStr(values=[Constant(value='Tasty ', kind=None), "
                                               "FormattedValue(value=Name(id='food', ctx=Load(), annotation=None, type_comment=None), conversion=-1, format_spec=None), "
                                               "Constant(value='!', kind=None)]), "
                       "type_comment=None), "
                "Assign(targets=[Name(id='template', ctx=Store(), annotation=None, type_comment=None)], "
                       "value=TemplateStr(values=[Constant(value='Tasty ', kind=None), "
                                                 "Interpolation(value=Name(id='food', ctx=Load(), annotation=None, type_comment=None), str='food', conversion=-1, format_spec=None), "
                                                 "Constant(value='!', kind=None)]), "
                       "type_comment=None)"
            "], type_ignores=[])")
        self.assertEqual(dump(tree), norm)

if sys.version_info < (3, 14):
    del Python3_14TestCase

if __name__ == '__main__':
    unittest.main()

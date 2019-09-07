import glob
import os
import unittest

import astunparse

import gast


class SelfTestCase(unittest.TestCase):

    def setUp(self):
        self.srcs = glob.glob(os.path.join(gast.__path__[0], '*.py'))

    def testParse(self):
        for src_py in self.srcs:
            with open(src_py) as f:
                content = f.read()
            gast.parse(content)

    def testCompile(self):
        for src_py in self.srcs:
            with open(src_py) as f:
                content = f.read()
            gnode = gast.parse(content)
            compile(gast.gast_to_ast(gnode), src_py, 'exec')

    def test_unparse(self):
        for src_py in self.srcs:
            with open(src_py) as f:
                content = f.read()
            gnode = gast.parse(content)
            astunparse.unparse(gast.gast_to_ast(gnode))


if __name__ == '__main__':
    unittest.main()

import unittest
import os
from models import Result

class ValidatorTestCase(unittest.TestCase):
    def testParser(self):
        path = os.path.join(os.path.dirname(__file__), 'test.galaxy')
        result = Result(input=open(path, 'r').read())
        output = result.process()
        print output

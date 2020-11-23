import unittest
from voiceProcessing import TestVoiceProcessing
from naturalLanguageProcessing import TestNLP
from pathFindingProcessing import TestPathFinding


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == "__main__":
    unittest.main()
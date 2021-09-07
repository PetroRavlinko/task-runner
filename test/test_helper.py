import unittest
import helper


class TestTaskRunnerMethods(unittest.TestCase):

    def setUp(self):
        self.unit = helper.Task()

    def test_str(self):
        self.assertEqual('Task: helper.py', str(self.unit))


if __name__ == '__main__':
    unittest.main()

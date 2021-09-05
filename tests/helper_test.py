import unittest
import helper


class TestTaskMethods(unittest.TestCase):

    def setUp(self):
        self.unit = helper.Task({})

    def test_str(self):
        self.assertEqual('Task: helper.py', str(self.unit))

    def test_add_subtask(self):
        self.unit.add_subtask(helper.Task({}))
        self.assertEqual(1, len(self.unit.subtasks))


if __name__ == '__main__':
    unittest.main()

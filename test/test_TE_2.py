import unittest
import TE_2


class TestTask2Methods(unittest.TestCase):

    def test_task_rollback(self):
        TE_2.rollback()


if __name__ == '__main__':
    unittest.main()

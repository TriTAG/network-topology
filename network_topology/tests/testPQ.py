import unittest
from network_topology.match import PriorityQueue


class QueueTestCase(unittest.TestCase):

    def setUp(self):
        self.q = PriorityQueue()

    def test_pop_empty_error(self):
        with self.assertRaises(KeyError):
            self.q.pop()

    def test_empty(self):
        self.assertTrue(self.q.empty(), 'queue is not empty')

    def test_pop1(self):
        self.q.add_or_update(1)
        self.assertEqual(self.q.pop(), 1, 'queue did not pop expected value')
        self.assertTrue(self.q.empty(), 'queue is not empty')

    def test_remove(self):
        self.q.add_or_update(1)
        self.q.add_or_update(2)
        self.q.add_or_update(3)
        self.q.remove(2)
        vals = []
        while not self.q.empty():
            vals.append(self.q.pop())
        self.assertNotIn(2, vals, 'queue still returned 2')

    def test_raise_priority(self):
        self.q.add_or_update(1, 4)
        self.q.add_or_update(2, 10)
        self.q.add_or_update(2, 1)
        self.assertEqual(self.q.pop(), 2, 'queue did not pop expected value')

    def test_lower_priority(self):
        self.q.add_or_update(1, 4)
        self.q.add_or_update(2, 10)
        self.q.add_or_update(1, 11)
        self.assertEqual(self.q.pop(), 2, 'queue did not pop expected value')

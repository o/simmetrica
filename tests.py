import mock
import unittest
import sys

sys.path.append('../')

from simmetrica import Simmetrica


class TestSimmetrica(unittest.TestCase):

    def setUp(self):
        self.simmetrica = Simmetrica()

    def test_push(self):
        self.assertEqual(8, len(self.simmetrica.push('foo')))

    def test_round_time(self):
        rounded_time = self.simmetrica.round_time(1363599249, 3600)
        self.assertEqual(rounded_time, 1363597200)

    def test_get_event_key(self):
        key = self.simmetrica.get_event_key('foo', '5min')
        self.assertEqual('simmetrica:foo:5min', key)

if __name__ == '__main__':
    unittest.main()

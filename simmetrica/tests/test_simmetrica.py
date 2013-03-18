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
        self.assertEqual(1363597200, self.simmetrica.round_time(1363599249, 3600))

    def test_get_event_key(self):
        self.assertEqual('simmetrica:foo:5min', self.simmetrica.get_event_key('foo', '5min'))

if __name__ == '__main__':
     unittest.main()

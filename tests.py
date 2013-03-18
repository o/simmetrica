import mock
import unittest
import sys

sys.path.append('../')

from simmetrica import Simmetrica


class TestSimmetrica(unittest.TestCase):

    def test_push(self):
        with mock.patch('simmetrica.StrictRedis') as StrictRedis:
            simmetrica = Simmetrica()
            hincrby = StrictRedis.return_value.pipeline.return_value.hincrby
            simmetrica.push('foo')
            self.assertTrue(hincrby.called)

    def test_round_time(self):
        simmetrica = Simmetrica()
        rounded_time = simmetrica.round_time(1363599249, 3600)
        self.assertEqual(rounded_time, 1363597200)

    def test_get_event_key(self):
        simmetrica = Simmetrica()
        key = simmetrica.get_event_key('foo', '5min')
        self.assertEqual('simmetrica:foo:5min', key)

if __name__ == '__main__':
    unittest.main()

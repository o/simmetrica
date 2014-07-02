import mock
import unittest
import sys

from simmetrica import Simmetrica


class TestSimmetrica(unittest.TestCase):

    def test_push(self):
        with mock.patch('simmetrica.simmetrica.StrictRedis') as StrictRedis:
            simmetrica = Simmetrica()
            hincrby = StrictRedis.return_value.pipeline.return_value.hincrby
            simmetrica.push('foo')
            self.assertTrue(hincrby.called)

    def test_get_timestamps_for_query(self):
        simmetrica = Simmetrica()
        timestamps = simmetrica.get_timestamps_for_query(1363707480, 1363707780, 60)
        self.assertEqual(timestamps, [1363707480, 1363707540, 1363707600, 1363707660, 1363707720])

    def test_get_timestamps_for_push(self):
        simmetrica = Simmetrica()
        timestamps = list(simmetrica.get_timestamps_for_push(1363707716))
        self.assertEqual(timestamps, [('week', 1363219200), ('hour', 1363705200), ('min', 1363707660), ('month', 1363392000), ('5min', 1363707600), ('year', 1356048000), ('day', 1363651200), ('15min', 1363707000)])

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from redis import StrictRedis, ConnectionError


class Config(object):
    pass


class Simmetrica(object):

    resolutions = {
        'min': 60,
        '5min': 300,
        '30min': 1800,
        'hour': 3600,
        'day': 86400,
        'week': 86400 * 7,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    def __init__(self, host='localhost', port=6379, db=0):
        self.backend = StrictRedis(host=host, port=port, db=db)

    def push(self, event, increment=1):
        pipe = self.backend.pipeline()
        for resolution, timestamp in self.get_timestamps_for_push():
            key = self.get_event_key(event, resolution)
            pipe.hincrby(key, timestamp, increment)
        return pipe.execute()

    def query(self, event, start, end, resolution='5min'):
        key = self.get_event_key(event, resolution)
        timestamps = self.get_timestamps_for_query(
            start, end, self.resolutions[resolution])
        return self.backend.hmget(key, timestamps)

    def get_timestamps_for_query(self, start, end, resolution):
        return range(self.round_time(start, resolution),
                     self.round_time(end, resolution),
                     resolution)

    def get_timestamps_for_push(self, now=None):
        now = now or int(time.time())
        for resolution, timestamp in self.resolutions.items():
            yield resolution, self.round_time(now, timestamp)

    def round_time(self, time, resolution):
        return int(time - (time % resolution))

    def get_event_key(self, event, resolution):
        return 'simmetrica:{0}:{1}'.format(event, resolution)

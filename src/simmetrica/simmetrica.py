#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from redis import StrictRedis


class Simmetrica(object):

    DEFAULT_INCREMENT = 1
    DEFAULT_RESOLUTION = '5min'
    DEFAULT_REDIS_HOST = 'localhost'
    DEFAULT_REDIS_PORT = 6379
    DEFAULT_REDIS_DB = 0
    DEFAULT_REDIS_PASSWORD = None

    resolutions = {
        'min': 60,
        '5min': 300,
        '15min': 900,
        'hour': 3600,
        'day': 86400,
        'week': 86400 * 7,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    def __init__(self, host=None, port=None, db=None, password=None):
        self.backend = StrictRedis(
            host=host or self.DEFAULT_REDIS_HOST,
            port=int(port or self.DEFAULT_REDIS_PORT),
            db=db or self.DEFAULT_REDIS_DB,
            password=password or self.DEFAULT_REDIS_PASSWORD
        )

    def push(self, event, increment=DEFAULT_INCREMENT, now=None):
        pipe = self.backend.pipeline()
        for resolution, timestamp in self.get_timestamps_for_push(now):
            key = self.get_event_key(event, resolution)
            pipe.hincrby(key, timestamp, increment)
        return pipe.execute()

    def query(self, event, start, end, resolution=DEFAULT_RESOLUTION):
        key = self.get_event_key(event, resolution)
        timestamps = self.get_timestamps_for_query(
            start, end, self.resolutions[resolution])
        values = self.backend.hmget(key, timestamps)
        for timestamp, value in zip(timestamps, values):
            yield timestamp, value or 0

    def get_timestamps_for_query(self, start, end, resolution):
        return range(self.round_time(start, resolution),
                     self.round_time(end, resolution),
                     resolution)

    def get_timestamps_for_push(self, now):
        now = now or self.get_current_timestamp()
        for resolution, timestamp in self.resolutions.items():
            yield resolution, self.round_time(now, timestamp)

    def round_time(self, time, resolution):
        return int(time - (time % resolution))

    def get_event_key(self, event, resolution):
        return 'simmetrica:{0}:{1}'.format(event, resolution)

    def get_current_timestamp(self):
        return int(time.time())

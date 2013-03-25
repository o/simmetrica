#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from simmetrica import Simmetrica

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='subparser_name')

push_parser = subparsers.add_parser('push')
push_parser.add_argument('event')
push_parser.add_argument('--increment', default=Simmetrica.DEFAULT_INCREMENT, type=int)
push_parser.add_argument('--now', type=int)

query_parser = subparsers.add_parser('query')
query_parser.add_argument('event')
query_parser.add_argument('start', type=int)
query_parser.add_argument('end', type=int)
query_parser.add_argument('--resolution', default='5min', choices=Simmetrica.resolutions)

args = parser.parse_args()

simmetrica = Simmetrica(
    os.getenv('REDIS_HOST'),
    os.getenv('REDIS_PORT'),
    os.getenv('REDIS_DB')
)

if args.subparser_name == 'push':
    simmetrica.push(args.event, args.increment, args.now)
    print 'ok'

if args.subparser_name == 'query':
    results = simmetrica.query(args.event, args.start, args.end, args.resolution)
    for timestamp, value in results:
        print timestamp, value

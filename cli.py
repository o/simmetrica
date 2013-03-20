#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from simmetrica import Simmetrica

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='subparser_name')

push_parser = subparsers.add_parser('push')
push_parser.add_argument('event')
push_parser.add_argument('--increment', default=1, type=int)

query_parser = subparsers.add_parser('query')
query_parser.add_argument('event')
query_parser.add_argument('start', type=int)
query_parser.add_argument('end', type=int)
query_parser.add_argument('--resolution', default='5min', choices=Simmetrica.resolutions)

args = parser.parse_args()

simmetrica = Simmetrica()

if args.subparser_name == 'push':
    simmetrica.push(args.event, args.increment)
    print 'ok'

if args.subparser_name == 'query':
    results = simmetrica.query(args.event, args.start, args.end, args.resolution)
    for timestamp, value in results:
        print timestamp, value

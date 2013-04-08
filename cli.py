#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from simmetrica import Simmetrica

parser = argparse.ArgumentParser(
    description='Starts Simmetrica commandline interface'
)

redis_arg_parser = argparse.ArgumentParser(add_help=False)
redis_arg_parser.add_argument(
    '--redis_host',
    '-rh',
    default=None,
    help='Connect to redis on the specified host'
)
redis_arg_parser.add_argument(
    '--redis_port',
    '-rp',
    default=None,
    help='Connect to redis on the specified port'
)
redis_arg_parser.add_argument(
    '--redis_db',
    '-rd',
    default=None,
    help='Connect to the specified db in redis'
)

redis_arg_parser.add_argument(
    '--redis_password',
    '-ra',
    default=None,
    help='Authorization password of redis'
)

subparsers = parser.add_subparsers(dest='subparser_name')

push_parser = subparsers.add_parser('push', parents=[redis_arg_parser])
push_parser.add_argument('event')
push_parser.add_argument(
    '--increment',
    default=Simmetrica.DEFAULT_INCREMENT,
    type=int
)
push_parser.add_argument('--now', type=int)

query_parser = subparsers.add_parser('query', parents=[redis_arg_parser])
query_parser.add_argument('event')
query_parser.add_argument('start', type=int)
query_parser.add_argument('end', type=int)
query_parser.add_argument(
    '--resolution',
    default='5min',
    choices=Simmetrica.resolutions
)

args = parser.parse_args()

simmetrica = Simmetrica(
    args.redis_host,
    args.redis_port,
    args.redis_db,
    args.redis_password
)

if args.subparser_name == 'push':
    simmetrica.push(args.event, args.increment, args.now)
    print 'ok'

if args.subparser_name == 'query':
    results = simmetrica.query(
        args.event,
        args.start,
        args.end,
        args.resolution
    )
    for timestamp, value in results:
        print timestamp, value

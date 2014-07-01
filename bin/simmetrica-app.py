#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
import re
import argparse
import os
import sys

from collections import OrderedDict

from flask import Flask, Response, request, render_template
from simmetrica import Simmetrica

default_config_filename = 'config.yml'
data_file_path=os.path.join(sys.prefix, 'share', 'doc', 'simmetrica')

parser = argparse.ArgumentParser(
    description='Starts Simmetrica web application'
)
parser.add_argument(
    '--debug',
    '-d',
    default=False,
    help='Run the app in debug mode',
    action='store_true'
)
parser.add_argument(
    '--config',
    '-c',
    default=default_config_filename,
    help='Run with the specified config file (default: config.yml)'
)
parser.add_argument(
    '--redis_host',
    '-rh',
    default=None,
    help='Connect to redis on the specified host'
)
parser.add_argument(
    '--redis_port',
    '-rp',
    default=None,
    help='Connect to redis on the specified port'
)
parser.add_argument(
    '--redis_db',
    '-rd',
    default=None,
    help='Connect to the specified db in redis'
)

parser.add_argument(
    '--redis_password',
    '-ra',
    default=None,
    help='Authorization password of redis'
)

args = parser.parse_args()

app = Flask(
    __name__, 
    static_folder=os.path.join(data_file_path, 'static'), 
    template_folder=os.path.join(data_file_path, 'templates')
)

simmetrica = Simmetrica(
    args.redis_host,
    args.redis_port,
    args.redis_db,
    args.redis_password
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/push/<event>')
def push(event):
    increment = request.args.get('increment') or Simmetrica.DEFAULT_INCREMENT
    now = int(request.args.get('now')) if request.args.get('now') else None
    simmetrica.push(event, increment, now)
    return 'ok'


@app.route('/query/<event>/<int:start>/<int:end>')
def query(event, start, end):
    resolution = request.args.get('resolution') or Simmetrica.DEFAULT_RESOLUTION
    result = simmetrica.query(event, start, end, resolution)
    response = json.dumps(OrderedDict(result))
    return Response(response, status=200, mimetype='application/json')


@app.route('/graph')
def graph():
    config_file = get_config_filename(args.config)
    stream = file(config_file)
    config = yaml.load(stream)
    result = []
    now = simmetrica.get_current_timestamp()
    for section in config['graphs']:
        timespan_as_seconds = get_seconds_from_relative_time(section.get('timespan', '1 day'))
        events = []
        for event in section['events']:
            data = simmetrica.query(event['name'], now - timespan_as_seconds, now, section.get('resolution', Simmetrica.DEFAULT_RESOLUTION))
            series = [dict(x=timestamp, y=int(value)) for timestamp, value in data]
            events.append(dict(
                name=event['name'],
                title=event.get('title', event['name']),
                data=series
            ))
        result.append(dict(
            title=section.get('title'),
            colorscheme=section.get('colorscheme', 'colorwheel'),
            type=section.get('type', 'area'),
            interpolation=section.get('interpolation', 'cardinal'),
            resolution=section.get('resolution', Simmetrica.DEFAULT_RESOLUTION),
            size=section.get('size', 'M'),
            offset=section.get('offset', 'value'),
            events=events,
            identifier='graph-' + str(id(events))
        ))
    response = json.dumps(result, indent=2)
    return Response(response, status=200, mimetype='application/json')

unit_multipliers = {
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'week': 86400 * 7,
    'month': 86400 * 30,
    'year': 86400 * 365
}


def get_seconds_from_relative_time(string):
    for unit in unit_multipliers.keys():
        if string.endswith(unit):
            match = re.match(r"(\d+)+\s(\w+)", string)
            if match:
                return unit_multipliers[unit] * int(match.group(1))
    else:
        raise ValueError("Invalid unit '%s'" % string)

def get_system_wide_config_filename():
    if hasattr(sys, 'real_prefix') or 'bsd' in sys.platform:
        return os.path.join(sys.prefix, 'etc', 'simmetrica', default_config_filename)
    elif not hasattr(sys, 'real_prefix') and 'linux' in sys.platform:
        return os.path.join('/etc', 'simmetrica', default_config_filename)
    elif 'darwin' in sys.platform:
        return os.path.join('/usr/local', 'etc', 'simmetrica', default_config_filename)
    elif 'win32' in sys.platform:
        return os.path.join(os.environ.get('APPDATA'), 'simmetrica', default_config_filename)

def get_config_filename(arg):
    current_dir = str(os.getcwd)
    if os.path.isfile(arg):
        return arg
    elif os.path.isfile(os.path.join(current_dir, arg)):
        return os.path.join(current_dir, arg)
    elif os.path.isfile(get_system_wide_config_filename()):
        return get_system_wide_config_filename()
    else:
        raise IOError("config.yml not found")

if __name__ == '__main__':
    app.run(debug=args.debug)

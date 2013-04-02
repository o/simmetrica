#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
import time
import re
import os
import argparse
 
from collections import OrderedDict

from flask import Flask, Response, request, render_template
from simmetrica import Simmetrica

parser = argparse.ArgumentParser(description='Start Simmetrica web application')
parser.add_argument('-c', '--config', dest='configFile', default='config.yml',
                   help='Run with the specified config file (default: config.yml)')
args = parser.parse_args()

app = Flask(__name__)
simmetrica = Simmetrica(
    os.getenv('REDIS_HOST'),
    os.getenv('REDIS_PORT'),
    os.getenv('REDIS_DB')
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
    stream = file(args.configFile)
    config = yaml.load(stream)
    result = []
    now = simmetrica.get_current_timestamp()
    for section in config['graphs']:
        timespan_as_seconds = get_seconds_from_relative_time(section.get('timespan', '1 day'))
        events = []
        for event in section['events']:
            data = simmetrica.query(event['name'], now - timespan_as_seconds, now, section.get('resolution', Simmetrica.DEFAULT_RESOLUTION))
            series = [ dict(x=timestamp, y=int(value)) for timestamp, value in data]
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
    'minute' : 60,
    'hour' : 3600,
    'day' : 86400,
    'week' : 86400 * 7,
    'month': 86400 * 30,
    'year' : 86400 * 365
}

def get_seconds_from_relative_time(string):
    for unit in unit_multipliers.keys():
        if string.endswith(unit):
            match = re.match(r"(\d+)+\s(\w+)", string)
            if match:
                return unit_multipliers[unit] * int(match.group(1))
    else: raise ValueError("Invalid unit '%s'" % string)

if __name__ == '__main__':
    app.run()

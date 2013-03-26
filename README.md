![build status](https://travis-ci.org/import/simmetrica.png?branch=master)

#Simmetrica (simple-metric-aggregator)

Simmetrica is a lightweight framework for collecting and aggregating event metrics as timeseries data. It also comes with beautiful customizable dashboard for visualizing metrics with charts.

![preview](http://import.github.com/assets/simmetrica/preview.png)

###Dependencies

* Python 2.6 or greater
* Redis Server

Most current Linux distributions (also Mac OS X) comes with Python in the base packages. Simmetrica uses `redis` for storing data, you can install `redis-server` with your favorite package manager.

###Installing

    git://github.com/import/simmetrica.git
    cd simmetrica
    pip install -r requirements.txt

###Feeding your data
#####From library

You need to run `redis-server` before pushing events and querying stored data.

    >>> from simmetrica import Simmetrica
    >>> simmetrica = Simmetrica()
    >>> simmetrica.push('add-cart-action')
    [1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L]

#####From commandline
  
    ➜ python cli.py push add-cart-action
    ok
  
#####From REST

After running `app.py` 

    ➜ curl 127.0.0.1:5000/push/add-cart-action
    ok

Also you can override default `event count` and `time` in all interfaces.

###Querying data
#####From library

    >>> start = simmetrica.get_current_timestamp() - 600
    >>> end = simmetrica.get_current_timestamp()     
    >>> results = simmetrica.query('add-cart-action', start, end, 'min')
    >>> for time, val in results:
    ...     print time, val
    ... 
    1364297940 0
    1364298000 0
    1364298060 0
    1364298120 0
    1364298180 0
    1364298240 0
    1364298300 0
    1364298360 0
    1364298420 0
    1364298480 1
    1364298540 2

#####From commandline

    ➜ python cli.py query add-cart-action 1364297990 1364298608 --resolution=min
    1364297940 0
    1364298000 0
    1364298060 0
    1364298120 0
    1364298180 0
    1364298240 0
    1364298300 0
    1364298360 0
    1364298420 0
    1364298480 1
    1364298540 2

Beautify with [spark](http://zachholman.com/spark/)

    ➜ python cli.py query add-cart-action 1364297990 1364298608 --resolution=min | awk '{print $2}' | spark
    ▁▁▁▁▁▁▁▁▁▄█

#####From REST

After running `app.py` 

    ➜ curl "127.0.0.1:5000/query/add-cart-action/1364297990/1364298608?resolution=min" | python -mjson.tool
    {
        "1364297940": 0, 
        "1364298000": 0, 
        "1364298060": 0, 
        "1364298120": 0, 
        "1364298180": 0, 
        "1364298240": 0, 
        "1364298300": 0, 
        "1364298360": 0, 
        "1364298420": 0, 
        "1364298480": "1", 
        "1364298540": "2"
    }

`resolution` is an optional parameter and it defaults to `5min`.

###Configuring dashboard blocks

Dashboard is configured with `config.yml` file, this file have a yaml list called `graphs`. Graphs widgets rendered with lovely [rickshaw](https://github.com/shutterstock/rickshaw)(HTML5 + SVG and d3.js) library.

    graphs:
        - graph parameters
            - events
        - graph definition
            - events


##### Explanation of parameters

**title**

Title of graph block.

Optional: No

**timespan**

How many timespan of data will shown in graph. 

Possible values: `(NUMBER minute|hour|day|week|month|year)`
Optional: Yes
Default: `1 day`

**colorscheme**

Colorscheme of graph parts.

Possible values: `classic9`, `colorwheel`, `cool`, `munin`, `spectrum14`, `spectrum2000` and `spectrum2001`
Optional: Yes
Default: `colorwheel`

**type**

Type of graph.

Possible values: `area`, `stack`, `bar`, `line` and `scatterplot`
Optional: Yes
Default: `area`

**interpolation**

Line smoothing / interpolation method of graphs.

Possible values: `linear`, `step-after`, `cardinal` and `basis`
Optional: Yes
Default: `cardinal`

**resolution**

Resolution of values. 

Possible values: `min`, `5min`, `15min`, `hour`, `day`, `week`, `month`, `year`
Optional: Yes
Default: `5min`

**size**

Size of graph.

Possible values: `S`, `M`, `L` and `XL`
Optional: Yes
Default: `M`

**offset**

Graph offset base.
 
Possible values: `zero`, `wiggle`, `expand` and `value`
Optional: Yes
Default: `value`

**events**

Every graph must be have at least one graph definition for rendering. Events have 2 values called `name`, and `title`. 

**name** 

This is the name of event, must be given.

**title**

Title of event, this will be shown in legend and not a mandatory value.

Typical graph block looks like this:

    - title: Title (mandatory)
      timespan: [10 minute, 3 hour, 2 day, 6 week, 1 month or whatever]
      colorscheme: [classic9, colorwheel, cool, munin, spectrum14, spectrum2000, spectrum2001]
      type: [area, stack, bar, line, scatterplot]
      interpolation: [linear, step-after, cardinal, basis]
      resolution: [min, 5min, 15min, hour, day, week, month, year]
      size: [S, M, L, XL]
      offset: [zero, wiggle, expand, value]
      events:
          - name: event_name (mandatory)
            title: Event Title

###Known issues

* Timezone is not adjustable for Time based axis [shutterstock/rickshaw#140](https://github.com/shutterstock/rickshaw/issues/140)

###Contributing

I just created this project for learning some Python. Please help me to make it better!

License
-------
Copyright (c) 2013 Osman Ungur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

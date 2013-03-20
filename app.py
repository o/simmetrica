from flask import Flask, jsonify
from simmetrica import Simmetrica

app = Flask(__name__)
simmetrica = Simmetrica()

@app.route('/')
def index():
    return 'Index page'

@app.route('/push/<event>/<increment>')
def push(event, increment):
    simmetrica.push(event, increment)
    return 'ok'

@app.route('/query/<event>/<int:start>/<int:end>', defaults={'resolution': '5min'})
@app.route('/query/<event>/<int:start>/<int:end>/<resolution>')
def query(event, start, end, resolution):
    result = simmetrica.query(event, start, end, resolution)
    response = jsonify(result)
    return response

if __name__ == '__main__':
    app.run()

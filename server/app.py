from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!<p>'

@app.route('/experiment', methods=['GET'])
def experiment():
    return '<p>/experiment hit<p>'

@app.route('/experiment/start', methods=['POST'])
def experiment_start():
    print(request.json)
    return '<p>/experiment/start hit<p>'

@app.route('/experiment/stop', methods=['PUT'])
def experiment_stop():
    return '<p>/experiment/stop hit<p>'

@app.route('/experiment/cycle', methods=['PUT'])
def experiment_cycle():
    return '<p>/experiment/cycle hit<p>'

if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)
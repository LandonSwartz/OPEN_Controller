from flask import Flask, request

app = Flask(__name__)

# This section is for checking if the server is reachable
@app.route('/')
def hello_world():
    return '<p>Hello, World!<p>'

# This section gets information about the current experiment
@app.route('/experiment', methods=['GET'])
def experiment():

    print(request)

    return '<p>/experiment hit<p>'

# This section starts a new experiment
@app.route('/experiment/start', methods=['POST'])
def experiment_start():
    
    print(request.json)
    
    return '<p>/experiment/start hit<p>'

# This section stops the current experiment
@app.route('/experiment/stop', methods=['PUT'])
def experiment_stop():
    
    return '<p>/experiment/stop hit<p>'

# This section (single) cycles the current experiment
@app.route('/experiment/cycle', methods=['PUT'])
def experiment_cycle():
    
    return '<p>/experiment/cycle hit<p>'

if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)
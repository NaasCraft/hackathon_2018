from flask import Flask
from flask import request

app = Flask(__name__)


HOST = '127.0.0.1'
PORT = 5444
SENSORID_JSON = 'sensorID'
TIMESTAMP_JSON = 'timestamp'
EVENT_ROUTE = '/event'
RESPONSE_STR = 'OK\n'


@app.route(EVENT_ROUTE, methods=['POST'])
def event():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        event()
        return RESPONSE_STR
        
def event():
    return
    
if __name__ == '__main__':
    app.run(host=HOST, port=PORT ,debug=True)
from flask import Flask, request, abort
from database import db, Game, GoalEvent

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5444
RESPONSE_STR = 'OK\n'


@app.route('/goal', methods=['POST'])
def goal():
    if request.method != 'POST':
        abort(401)
        return
    json_data = request.get_json(force=True)
    return RESPONSE_STR


def main():
    db.init_app(app)
    app.run(host=HOST, port=PORT, debug=True)
    db.create_all()


if __name__ == '__main__':
    main()

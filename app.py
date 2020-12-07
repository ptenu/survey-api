import os
import yaml
from flask import Flask, request
from ex import db
from models import Submission
from flask_limiter import Limiter
from flask_cors import CORS
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

CORS(app)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/', methods=['GET'])
@limiter.exempt
def get_questions():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(dir_path, 'survey.yml')
    with open(yaml_path) as file:
        questions = yaml.load(file, Loader=yaml.FullLoader)

        return {
            "questions": questions["questions"]
        }, 200


@app.route('/submit', methods=['POST'])
@limiter.limit("5/day;1/minute")
def save_response():
    data = request.get_json()
    if data is None:
        return {"error": "No request data."}, 400
    s = Submission(data)
    db.session.add(s)
    db.session.commit()

    return {
        "id": s.id
    }, 201


if __name__ == '__main__':
    app.run()

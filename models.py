import datetime
import os
import random
import yaml
from string import ascii_letters, hexdigits, digits

from ex import db


class Response(db.Model):
    """
    Model for storing the answer to each question
    """

    submission_id = db.Column(
        db.String(50),
        db.ForeignKey('submission.id'),
        primary_key=True
    )

    field = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.Text, nullable=False)

    def __init__(self, submission, field, value):
        self.submission_id = submission.id
        self.field = field
        self.value = str(value)


class Submission(db.Model):
    """
    Model for storing survey submissions
    """

    id = db.Column(db.String(50), primary_key=True)
    set = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)

    fields = db.relationship(Response, backref='submission', lazy=False)

    def __init__(self, data):
        self.date = datetime.date.today()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(dir_path, 'survey.yml')
        with open(yaml_path) as file:
            questions = yaml.load(file, Loader=yaml.FullLoader)
            self.set = questions["version"]
            self.set_id()

            allowed_fields = []
            for f in questions["questions"]:
                allowed_fields.append(f["field"])

            for field, value in data.items():
                if field not in allowed_fields:
                    continue
                if value == "":
                    continue

                if value[0] in digits and value[1] in ('Y', 'N'):
                    value = value[1:]

                self.fields.append(Response(self, field, value))

    def get_field(self, field):
        return Response.query.get(self.id, field)

    def set_id(self):
        id = f's_{self.set}'

        id += random.choice(('-', '_'))

        for i in range(4):
            id += random.choice(hexdigits)

        for i in range(8):
            id += random.choice((*digits, *ascii_letters))

        self.id = id
        return id
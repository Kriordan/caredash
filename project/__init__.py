import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Load Env Vars
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Flask App Configuration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'caredash.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Model Definitions
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', lazy='select',
        backref=db.backref('doctor', lazy='joined'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Doctor %r>' % self.id


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __init(self, description, doctor):
        self.description = description
        self.doctor = doctor

    def __repr__(self):
        return '<Review %r>' % self.id


# Model Schemas
class DoctorSchema(ma.ModelSchema):
    class Meta:
        model = Doctor


class ReviewSchema(ma.ModelSchema):
    class Meta:
        model = Review


doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


# Routes
@app.route('/')
def home():
    return 'So it goes'


# API Endpoints
@app.route('/doctors', methods=['GET'])
def all_doctors():
    doctors = Doctor.query.all()

    result = doctors_schema.dump(doctors)
    return jsonify(result.data)


@app.route('/doctors', methods=['POST'])
def create_doctor():
    name = request.json['doctor']['name']
    doctor = Doctor(
        name=name
    )

    db.session.add(doctor)
    db.session.commit()

    result = doctor_schema.dump(Doctor.query.get(doctor.id))
    return jsonify(result.data)


@app.route('/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)

    result = doctor_schema.dump(doctor)
    return jsonify(result.data)


# @app.route('/doctors/<int:id>', methods=['PUT'])
# def update_doctor(id):
#     doctor = Doctor.query.get(id)


@app.route('/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)

    db.session.delete(doctor)
    db.session.commit()

    result = doctor_schema.dump(doctor)
    return jsonify(result.data)


# @app.route('/doctors/<int:id>/reviews', methods=['GET'])
# def all_reviews(id):
#     reviews = Reviews.query.filter_by()


@app.route('/doctors/<int:doctor_id>/reviews', methods=['POST'])
def create_reviews(doctor_id):
    description = request.json['review']['description']
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return jsonify({'message': 'No doctor found'}), 400

    review = Review(
        description=description,
        doctor=doctor
    )

    db.session.add(review)
    db.session.commit()

    result = review_schema.dump(Review.query.get(review.id))
    return jsonify(result.data)


@app.route('/doctors/<int:doctor_id>/reviews/<int:id>', methods=['GET'])
def get_review(doctor_id, id):
    review = Review.query.get(id)

    result = review_schema.dump(review)
    return jsonify(result.data)


@app.route('/doctors/<int:doctor_id>/reviews/<int:id>', methods=['DELETE'])
def delete_review(doctor_id, id):
    review = Review.query.get(id)

    db.session.delete(review)
    db.session.commit()

    result = review_schema.dump(review)
    return jsonify(result.data)
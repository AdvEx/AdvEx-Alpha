import os
import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


DB_URL = os.environ['SQLALCHEMY_DATABASE_URI']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

SAMPLE_FEEDBACK = {
    "rating": "Good", 
    "robustness": "9", 
    "details": [
        {
            "attack_method": "CLEAN", 
            "confidence": "95%", 
            "accuracy": "80.05%"
        }, 
        {
            "attack_method": "FGSM", 
            "confidence": "95%", 
            "accuracy": "80.05%"
        }, 
        {
            "attack_method": "MI-FGSM", 
            "confidence": "91%", 
            "accuracy": "92.10%"
        }, 
        {
            "attack_method": "I-FGSM", 
            "confidence": "93.7%", 
            "accuracy": "94.10%"
        }
    ], 
    "suggestion": "Your model can be made more robust by training it with adversarial examples.", 
}


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(200), unique=False, nullable=False)
	email = db.Column(db.String(200), unique=True, nullable=False)
	password = db.Column(db.String(200), unique=False, nullable=False)

	def __repr__(self):
		return '<User ID: {}, nickname: {}, email: {}>'.format(self.user_id, 
			self.nickname, self.email)


class Submission(db.Model):
	submission_id = db.Column(db.Integer, primary_key=True)
	model_name = db.Column(db.String(80), nullable=False)
	status = db.Column(db.String(80), nullable=False)
	s3_model_key = db.Column(db.String(80), nullable=False)
	s3_index_key = db.Column(db.String(80), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	feedback = db.Column(JSON, nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	user = db.relationship('User', backref=db.backref('submissions', lazy=True), uselist=False)

	def __repr__(self):
		return '<Submission ID: {}, model_name: {}, status: {}, model_key: {}, index_key: {}, created_at: {}>'\
			.format(self.submission_id, self.model_name, self.status, self.s3_model_key, self.s3_index_key, self.created_at)


def init_db():
	print('Drop')
	db.drop_all()
	print('Create')
	db.create_all()

	user1 = User(
		nickname='Dave',
		email='dave@gmail.com',
		password='aircrash'
	)

	user2 = User(
		nickname='Nancy',
		email='nrmcmu@gmail.com',
		password='H2F0WGDF'
	)

	user3 = User(
		nickname='Andrew',
		email='andrew.mellinger@gmail.com',
		password='S2GHZ5UI'
	)

	user4 = User(
		nickname='Oren',
		email='owright@sei.cmu.edu',
		password='7RHX95O5'
	)

	user5 = User(
		nickname='Gregory',
		email='laidlags@udmercy.edu',
		password='EAHDTU3P'
	)

	submission1 = Submission(
		user_id=1,
		model_name='VGG-16 v1.0',
		status='Finished',
		s3_model_key='model.h5',
		s3_index_key='index.json',
		feedback=SAMPLE_FEEDBACK
	)

	submission2 = Submission(
		user_id=1,
		model_name='VGG-16 v2.0',
		status='Failed',
		s3_model_key='model.h5',
		s3_index_key='index.json',
		feedback={"error": "Model file too large."}
	)

	# submission3 = Submission(
	# 	user_id=1,
	# 	model_name='VGG-16 v3.0',
	# 	status='Running',
	# 	s3_model_key='model.h5',
	# 	s3_index_key='index.json',
	# 	feedback={}
	# )

	# submission4 = Submission(
	# 	user_id=1,
	# 	model_name='VGG-16 v4.0',
	# 	status='Submitted',
	# 	s3_model_key='model.h5',
	# 	s3_index_key='index.json',
	# 	feedback={}
	# )

	db.session.add(user1)
	db.session.add(user2)
	db.session.add(user3)
	db.session.add(user4)
	db.session.add(user5)
	db.session.add(submission1)
	db.session.add(submission2)
	db.session.commit()


def test_alpha():
	feedback = Submission.query.get(1).feedback
	print(feedback if feedback else 'EMPTY FEEDBACK')


if __name__ == '__main__':
	if sys.argv[1] == 'init':
		init_db()
	if sys.argv[1] == 'test':
		test_alpha()

import boto3
import json
import time
from db import db, Submission


s3 = boto3.resource('s3')
bucket = s3.Bucket('advex')

sqs = boto3.client('sqs')
resp = sqs.get_queue_url(QueueName='advex')
queue_url = resp['QueueUrl']


SAMPLE_FEEDBACK = {
	"robustness": "9",
	"rating": "Good",
	"details": {
		"original_accuracy": "98.55%",
		"attack_results": [
			{
				"attack_method": "FGSM",
				"accuracy": "80.05%",
				"confidence": "95%"
			},
			{
				"attack_method": "Basic Iterative Method",
				"accuracy": "92.10%",
				"confidence": "91%"
			},
			{
				"attack_method": "Carlini Wagner",
				"accuracy": "94.10%",
				"confidence": "93%"
			},
			{
				"attack_method": "Momentum Iterative Method",
				"accuracy": "94.10%",
				"confidence": "93.7%"
			},
			{
				"attack_method": "DeepFool",
				"accuracy": "90.10%",
				"confidence": "89%"
			}
		]
	},
	"suggestion": "Your model can be made more robust by training it with some of the adversarial examples which you can download for free from your dashboard."
}


def write_feedback(submission_id, feedback):
	print('Writing feedback.')
	submission = Submission.query.get(submission_id)
	submission.feedback = feedback
	db.session.commit()


def evaluate_job(job):
	print('Evaluating model.')

	submission_id = job['submission_id']
	model_file = job['s3_model_key']
	index_file = job['s3_index_key']

	bucket.download_file(model_file, 'tmp/'+model_file)
	bucket.download_file(index_file, 'tmp/'+index_file)

	# Actual evaluation
	time.sleep(20)

	write_feedback(submission_id, SAMPLE_FEEDBACK)


def main():
	while True:
		resp = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
		if 'Messages' not in resp:
			print('No messages received, sleep for 10s.')
			time.sleep(10)
			continue

		print('Message received.')
		message = resp['Messages'][0]
		receipt_handle = message['ReceiptHandle']
		job = json.loads(message['Body'])

		# Process job
		evaluate_job(job)

		# Delete message
		resp = sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)


if __name__ == '__main__':
	main()

import boto3
import json
import time
from db import db


sqs = boto3.client('sqs')
resp = sqs.get_queue_url(QueueName='advex')
queue_url = resp['QueueUrl']


SAMPLE_JOB = {
	'submission_id': 1,
	's3_model_key': 'model.h5',
	's3_index_key': 'index.json'
}


def submit_job(job):
	message = json.dumps(job)
	resp = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
	print('Message sent with ID =', resp['MessageId'])


def main():
	submit_job(SAMPLE_JOB)


if __name__ == '__main__':
	main()

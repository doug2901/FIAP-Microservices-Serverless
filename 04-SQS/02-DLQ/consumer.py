from sqsHandler import SqsHandler
import time
sqs = SqsHandler('https://sqs.us-east-1.amazonaws.com/708096016377/demoqueue')

while(True):
    response = sqs.getMessage(10, 20)

    if('Messages' not in response):
        break

    for msg in response['Messages']:
        print(msg['MessageId'])
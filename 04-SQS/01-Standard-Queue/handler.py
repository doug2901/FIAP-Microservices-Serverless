from sqsHandler import SqsHandler
from env import Variables
import json


def handler(event, context):
    env = Variables()
    sqs = SqsHandler(env.get_sqs_url())
    sqs_dest = SqsHandler(env.get_sqs_url_dest())

    for i in range(100):
        msgs = sqs.getMessage(10)
        print(json.dumps(msgs))

        if('Messages' not in msgs):
            break
        if(len(msgs['Messages'])==0):
            break

        for message in msgs['Messages']:
            sqs_dest.send(json.dumps(message['Body']))
            sqs.deleteMessage(message['ReceiptHandle'])
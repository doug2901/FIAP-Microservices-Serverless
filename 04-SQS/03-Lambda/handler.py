import json
from sqsHandler import SqsHandler

AWS: Add Debug Configuration | AWS: Edit Debug Configuration (Beta)
def handler(event, context):

    print(json.dumps(event))

    sqs = SqsHandler("https://sqs.us-east-1.amazonaws.com/708096016377/demoqueue_dest")

    for record in event["Records"]:
        payload=record["body"]
        print(json.dumps(payload))
        sqs.send(payload)

    return event
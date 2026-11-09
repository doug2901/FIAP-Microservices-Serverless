import base64
import os

import boto3

from response import _response


sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]



def feedback(event, context):
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")

    try:
        response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=body)
    except Exception as erro:
        print(f"Erro ao enviar mensagem para a fila: {erro}")
        return _response(500, {"mensagem": "Não foi possível registrar o feedback."})

    return _response(
        200,
        {
            "mensagem": "Feedback recebido e enviado para processamento.",
            "messageId": response["MessageId"],
        },
    )
    
import json
import os

import boto3


TABLE_NAME = os.getenv("TABLE_NAME", "FeedbacksReclamacoes")
NOTIFICATION_TOPIC_ARN = os.environ.get("NOTIFICATION_TOPIC_ARN")

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
table = dynamodb.Table(TABLE_NAME)


def inserir_feedback(feedback):
    item = {
        "id_cliente": feedback["id_cliente"],
        "descricao": feedback["descricao"],
        "categoria": feedback["categoria"],
        "data_hora": feedback["data_hora"],
    }
    return table.put_item(Item=item)


def notificar_equipe(feedback):
    if not NOTIFICATION_TOPIC_ARN:
        raise RuntimeError("A variável NOTIFICATION_TOPIC_ARN não foi configurada.")

    return sns.publish(
        TopicArn=NOTIFICATION_TOPIC_ARN,
        Subject="Novo feedback recebido",
        Message=(
            "Novo feedback recebido.\n\n"
            f"Cliente: {feedback['id_cliente']}\n"
            f"Categoria: {feedback['categoria']}\n"
            f"Descrição: {feedback['descricao']}\n"
            f"Data/hora: {feedback['data_hora']}"
        ),
    )


def handler(event, context):
    for record in event.get("Records", []):
        body = record.get("body", "{}")
        feedback = json.loads(body)
        inserir_feedback(feedback)
        notificar_equipe(feedback)

    return {"statusCode": 200, "body": json.dumps({"processados": len(event.get('Records', []))})}

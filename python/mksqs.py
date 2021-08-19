"""
Send messages into AWS SQS queues.

return dict
"""
import json
import boto3


def sendmessage(queue_url: str, message: dict) -> dict:
    """
    Send messages into AWS SQS queues.

    return dict
    """
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

    return response

"""
Send AWS SNS notifications.

return None
"""
import boto3


def notify(topic: str, message: str, subject: str) -> None:
    """
    Send AWS SNS notifications.

    return None
    """
    sns = boto3.client('sns')
    responsesns = sns.publish(
        TopicArn=topic,
        Message=message,
        Subject=subject
    )

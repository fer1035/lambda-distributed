"""Send SNS notifications for SQS dead-letter queue."""
import os
import re
import json
import mksns  # [internal]


def lambda_handler(event, context):
    """Send SNS notifications for SQS dead-letter queue."""
    try:

        # Get data from SQS queue.
        for record in event['Records']:
            data = json.loads(record['body'])['data']

        # Validate data syntax.
        if not re.match(r'^[\w]+$', data):
            raise Exception(
                'Invalid data syntax. '
                'Only alphanumeric characters and underscores are allowed.'
            )

        # Send notifications.
        mksns.notify(
            os.environ['SNSTOPIC'],
            'Data: {}\n'
            'Exception: Failed to process after 5 tries'
            .format(data),
            os.environ['SNSSUBJECT']
        )

        # Create success return.
        status_code = 200
        status = 'Succeeded'

    except Exception as e:

        # Create failure return.
        status_code = 500
        status = 'Failed: {}'.format(str(e))

    # Return response.
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(
            {'message': status},
            default=str
        )
    }

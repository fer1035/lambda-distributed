"""Demonstrate distributed computing in Lambda (SQS)."""
import json
import os
import re
import mksqs  # [internal]


def lambda_handler(event, context):
    """
    Demonstrate distributed computing in Lambda (SQS).

    return dict
    """
    try:

        # Get data from API request body.
        data = json.loads(event['body'])['data']

        # Validate data syntax.
        if not re.match(r'^[\w]+$', data):
            raise Exception(
                'Invalid data syntax. '
                'Only alphanumeric characters and underscores are allowed.'
            )

        # Send data to SQS queue.
        response = mksqs.sendmessage(os.environ['SQSQUEUE'], {'data': data})

        # Create success return.
        status_code = 200
        status = (
            'Succeeded: {}'
            .format(
                data
            )
        )

        print(
            '{{"data": "{}", "status_code": {}}}'
            .format(
                data,
                status_code
            )
        )

    except Exception as e:

        # Null data value if no data is supplied.
        data = None

        # Create failure return.
        status_code = 500
        status = (
            'Failed: {}'
            .format(str(e))
        )

        print(
            '{{"status_code": {}, "exception": "{}"}}'
            .format(
                status_code,
                str(e)
            )
        )

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

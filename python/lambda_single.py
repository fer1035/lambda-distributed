"""Demonstrate single-node computing in Lambda."""
import boto3
import json
import os
import time
import re
import searchitems  # [internal]
import mkrandom  # [internal]


def lambda_handler(event, context):
    """
    Demonstrate single-node computing in Lambda.

    return dict
    """
    try:

        # Get data from SQS queue.
        data = json.loads(event['body'])['data']

        # Validate data syntax.
        if not re.match(r'^[\w]+$', data):
            raise Exception(
                'Invalid data syntax. '
                'Only alphanumeric characters and underscores are allowed.'
            )

        # Process data and send result to DynamoDB.
        id = (
            '{}_{}'
            .format(
                mkrandom.mkrandom(5),
                time.time()
            )
        )
        timestamp = str(
            time.strftime(
                "%Y-%m-%d:%H-%M-%S%Z",
                time.localtime()
            )
        )
        processed_data = (
            '{}_processed'
            .format(data)
        )

        # Send result to DynamoDB for storage.
        item = {
            'id': id,
            'timestamp': timestamp,
            'processed': processed_data
        }
        response = searchitems.putitem(
            os.environ['DBTABLE'],
            item
        )

        # Create success return.
        status_code = 200
        status = (
            'Succeeded: {}'
            .format(id)
        )

        print(
            '{{"data": "{}", "status_code": {}, "id": "{}"}}'
            .format(
                data,
                status_code,
                id
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
            '{{"data": "{}", "status_code": {}, "exception": "{}"}}'
            .format(
                data,
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

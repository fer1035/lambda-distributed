"""Execute DynamoDB operations."""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def batchgetitems(
    table1_name: str,
    table2_name: str,
    keydict1: dict,
    keydict2: dict
) -> dict:
    """
    Get items in batch from DynamoDB.

    return dict
    """
    dynamodb = boto3.resource('dynamodb')
    table1 = dynamodb.Table(table1_name)
    table2 = dynamodb.Table(table2_name)
    batch_keys = {
        table1.name: {
            'Keys': [keydict1]
        },
        table2.name: {
            'Keys': [keydict2]
        }
    }
    response = dynamodb.batch_get_item(
        RequestItems=batch_keys
    )

    return response['Items']


def getitem(
    table: str,
    key: str,
    value: str
) -> dict:
    """
    Get one item from DynamoDB.

    return dict
    """
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.Table(table).get_item(
        Key={
            key: value
        }
    )

    return response['Item']


def queryitems(
    table: str,
    key: str,
    value: str
) -> dict:
    """
    Get items based on keyword query from DynamoDB.

    return dict
    """
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.Table(table).query(
        KeyConditionExpression=Key(key).eq(value)
    )

    return response['Items']


def scanitems(
    table: str,
    key: str,
    value: str,
    patternexp: dict
) -> dict:
    """
    Get all items from a DynamoDB table then filter by expression.

    return dict
    """
    dynamodb = boto3.resource('dynamodb')
    fe = Key(key).eq(value)
    pe = patternexp
    response = dynamodb.Table(table).scan(
        FilterExpression=fe,
        ProjectionExpression=pe
    )

    return response['Items']


def scanallitems(
    table: str
) -> dict:
    """
    Get all items from a table in DynamoDB.

    return dict
    """
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.Table(table).scan()

    return response['Items']


def putitem(
    table: str,
    itemdict: dict
) -> None:
    """
    Put one item into DynamoDB.

    return None
    """
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.Table(table).put_item(
        Item=itemdict
    )


def deleteallitems(
    table: str
) -> None:
    """
    Delete all items from a DynamoDB table.

    return None
    """
    dynamodb = boto3.resource('dynamodb')
    response = dynamodb.Table(table).scan()
    with dynamodb.Table(table).batch_writer() as batch:
        for each in response['Items']:
            batch.delete_item(Key=each)


def deletetable(
    table: str
) -> None:
    """
    Delete a table from DynamoDB.

    return None
    """
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.describe_table(TableName=table)
        response = dynamodb.delete_table(TableName=table)
        waiter = dynamodb.get_waiter('table_not_exists')
        waiter.wait(
            TableName=table,
            WaiterConfig={
                'Delay': 5,
                'MaxAttempts': 10
            }
        )
    except Exception as e:
        pass


def createtable(
    table: str,
    attrdictls: list,
    schemadictls: list,
    kmsid: str,
    tagdictls: list
) -> None:
    """
    Create a table in DynamoDB.

    return None
    """
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.describe_table(TableName=table)
    except Exception as e:
        response = dynamodb.create_table(
            TableName=table,
            AttributeDefinitions=attrdictls,
            KeySchema=schemadictls,
            # BillingMode='PROVISIONED',
            # ProvisionedThroughput={
            #     'ReadCapacityUnits': 25,
            #     'WriteCapacityUnits': 25
            # },
            BillingMode='PAY_PER_REQUEST',
            SSESpecification={
                'Enabled': True,
                'SSEType': 'KMS',
                'KMSMasterKeyId': kmsid
            },
            Tags=tagdictls
        )
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(
            TableName=table,
            WaiterConfig={
                'Delay': 5,
                'MaxAttempts': 10
            }
        )


def updateitem(
    table: str,
    keydict: dict,
    attributedict: dict,
    valuedict: dict,
    updateexpression: str
) -> dict:
    """
    Update an item in a DynamoDB table.

    return dict
    """
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.update_item(
        TableName=table,
        Key=keydict,
        ExpressionAttributeNames=attributedict,
        ExpressionAttributeValues=valuedict,
        UpdateExpression=updateexpression
    )
    return response

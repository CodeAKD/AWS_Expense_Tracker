import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserET')

# Utility function to handle Decimal → float conversion
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    # Extract user email from Cognito identity (JWT claims)
    email = event["requestContext"]["authorizer"]["claims"]["email"]
    
    # Query all expenses for that user
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('mailId').eq(email)
    )

    items = response.get('Items', [])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps({"items": items}, default=decimal_default)
    }

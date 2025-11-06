import json, os, boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'UserET'))

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,DELETE"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    claims = event["requestContext"]["authorizer"]["claims"]
    email = claims["email"]

    body = json.loads(event.get("body", "{}"))
    expense_id = body.get("expense_id")
    if not expense_id:
        return response(400, {"error": "expense_id is required"})

    table.delete_item(Key={"mailId": email, "sortId": expense_id})
    return response(200, {"message": "Expense deleted"})

import json, os, boto3, uuid
from datetime import datetime

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
    # ID token claims from API Gateway authorizer
    claims = event["requestContext"]["authorizer"]["claims"]
    email = claims["email"]

    body = json.loads(event.get("body", "{}"))
    amount = body.get("amount")
    category = body.get("category")
    date = body.get("date")  # YYYY-MM-DD

    if amount is None or not category or not date:
        return response(400, {"error": "amount, category, date are required"})

    expense_id = f"EXPENSE#{datetime.utcnow().isoformat()}#{uuid.uuid4().hex[:8]}"

    item = {
        "mailId": email,
        "sortId": expense_id,
        "amount": amount,
        "category": category,
        "date": date
    }

    table.put_item(Item=item)
    return response(200, {"message": "Expense added", "expense_id": expense_id})

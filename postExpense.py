import json, os, boto3, uuid
from datetime import datetime
from decimal import Decimal

# Initialize AWS resources
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# Environment variables
TABLE_NAME = os.environ.get("TABLE_NAME", "UserET")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")
ALERT_THRESHOLD = Decimal(os.environ.get("ALERT_THRESHOLD", "10000"))

table = dynamodb.Table(TABLE_NAME)

# JSON response helper
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
    try:
        # Extract user email from Cognito authorizer claims
        claims = event["requestContext"]["authorizer"]["claims"]
        email = claims["email"]

        # Parse request body
        body = json.loads(event.get("body", "{}"))
        amount = body.get("amount")
        category = body.get("category")
        date = body.get("date")  # YYYY-MM-DD

        # Validate inputs
        if amount is None or not category or not date:
            return response(400, {"error": "amount, category, date are required"})

        # Convert to Decimal safely
        amount = Decimal(str(amount))

        # Create a unique sort key for this expense
        expense_id = f"EXPENSE#{datetime.utcnow().isoformat()}#{uuid.uuid4()}"

        # Insert into DynamoDB
        table.put_item(Item={
            "mailId": email,
            "sortId": expense_id,
            "amount": amount,
            "category": category,
            "date": date
        })

        # --- SNS ALERT LOGIC ---
        if SNS_TOPIC_ARN and amount > ALERT_THRESHOLD:
            subject = "High Expense Alert"
            message = (
                f"🚨 High Expense Alert 🚨\n\n"
                f"User: {email}\n"
                f"Amount: ₹{amount}\n"
                f"Category: {category}\n"
                f"Date: {date}\n"
                f"Expense ID: {expense_id}\n"
                f"\nThis expense exceeded your set threshold of ₹{ALERT_THRESHOLD}."
            )

            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=subject,
                    Message=message
                )
                print("SNS alert published successfully!")
            except Exception as sns_error:
                print("Failed to send SNS alert:", sns_error)

        # Return success response
        return response(200, {"message": "Expense added successfully", "expense_id": expense_id})

    except Exception as e:
        print("Error in Lambda:", e)
        return response(500, {"error": "Internal server error", "details": str(e)})

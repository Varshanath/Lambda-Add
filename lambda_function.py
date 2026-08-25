import json


def lambda_handler(event, context):
    """Add two numbers from an HTTP request."""
    try:
        query_parameters = event.get("queryStringParameters") or {}
        body = event.get("body")

        if body:
            if isinstance(body, str):
                body = json.loads(body)
            request_data = body
        else:
            request_data = query_parameters

        first_number = float(request_data["a"])
        second_number = float(request_data["b"])
        result = first_number + second_number

        if result.is_integer():
            result = int(result)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"result": result}),
        }
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Provide numeric values for a and b."}),
        }

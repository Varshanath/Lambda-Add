import json

from lambda_function import lambda_handler


def run(name, event):
    response = lambda_handler(event, None)
    body = json.loads(response["body"])
    print(f"{name}: statusCode={response['statusCode']} body={body}")


if __name__ == "__main__":
    run("GET query params", {"queryStringParameters": {"a": "2", "b": "3"}})
    run("POST JSON body (string)", {"body": json.dumps({"a": 2.5, "b": 1.5})})
    run("POST JSON body (dict)", {"body": {"a": 10, "b": -4}})
    run("Missing param", {"queryStringParameters": {"a": "2"}})
    run("Non-numeric value", {"queryStringParameters": {"a": "x", "b": "3"}})
    run("No input at all", {})

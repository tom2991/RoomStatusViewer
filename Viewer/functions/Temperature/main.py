import jinja2

# lambdaのハンドラ
def handle(event, context):
    print("print log.")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "Hello"
    }
def lambda_handler(event, context):
    print("print log.")
    return {
        "message": "Hello World",
    }
def personalization(event, context):
    """
    Args:
        event (dict) : The dictionary with data specific to this type of event.
        - The `data` field contains the PubsubMessage message.
        - The `attributes` field contains custom attributes if there are any.
        context (google.cloud.functions.Context) : The Cloud Functions event metadata.
        - The `event_id` field contains the Pub/Sub message ID.
        - The `timestamp` field contains the publish time.
    """

    import base64

    def fib(n):
        if n == 0 or n == 1:
            return n
        return fib(n - 1) + fib(n - 2)

    if 'data' in event:
        n = base64.b64decode(event['data']).decode('utf-8')
        result = fib(n)
        print(str(result))

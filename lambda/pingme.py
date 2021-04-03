import logging
import json

def handler(event, context):
    logging.info(event)
    payload = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': event["body"]
    }
    return payload

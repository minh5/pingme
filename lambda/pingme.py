import logging
import json
import os

import boto3


def handler(event, context):
    logging.info(event)
    sns_client = boto3.client("sns")

    # Put an event
    message = {"Message": event["body"], "TopicArn": os.environ["topic_arn"]}
    sns_client.publish(**message)

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'message successfully sent via Pingme'
    }
    return response

import logging
import json
import os

from typing import Any
from typing import Dict

import boto3


def handler(event: Dict[str, Any], context: Dict[str, Any]) -> None:
    """Taking the request from API Gateway, parse the message, and send it to
    the SNS topic that will send an SMS message

    The phone number for the SNS is set in an environmental variable that is
    used during deployment
    """
    logging.info(event)
    sns_client = boto3.client("sns")

    # Put an event
    message = {"Message": event["body"], "TopicArn": os.environ["topic_arn"]}
    response = {"headers": {"Content-Type": "text/plain"}}

    # this variable is required for deploy
    phone = os.environ["PHONE_NUMBER"]
    obfuscated = "X" * (len(phone) - 4) + phone[-4:]

    # validation
    try:
        sns_client.publish(**message)
        response["statusCode"] = 200
        response["body"] = f"message successfully sent via pingme to {obfuscated}"
    except Exception as e:
        response["statusCode"] = 400
        response["body"] = e
        logging.error()

    return response

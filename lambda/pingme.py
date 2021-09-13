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
    message = {"Message": event["body"], "TopicArn": os.environ["TOPIC_ARN"]}
    response = {"headers": {"Content-Type": "text/plain"}}

    # this variable is required for deploy
    phone = os.environ["PHONE_NUMBER"]
    obfuscated = "X" * (len(phone) - 4) + phone[-4:]

    data = """
    HELLO THIS THE FIRST CHALLENGE, parse this data frame

    +-----------+------------+----------+
    | 1 COLUMN  |  2 COLUMN  | 3 COLUMN |
    +-----------+------------+----------+
    | fake_id_1 | fake_id_2  |          |
    |           |            |          |
    | 5H22WPQY  | RZ0O44BBSL |          |
    |           |            |          |
    | QXX7AXCB  | N9UP27D7MZ |          |
    |           |            |          |
    | F1EW26N3  | SDI9N0TNH  |          |
    |           |            |          |
    | CX05VC50  | QO3QU2NJJ9 |          |
    |           |            |          |
    | QFVHGFWU  | LYXOBRKU3H |          |
    |           |            |          |
    | Z8E7WRIP  | MEOQQ91JN8 |          |
    |           |            |          |
    | 38ZNGKNM  | GLU8ORMSEP |          |
    |           |            |          |
    | B6ULQT9W  | 40RET4EK1E |          |
    +-----------+------------+----------+
    """
    # validation
    try:
        # sns_client.publish(**message)
        response["statusCode"] = 200
        # response["body"] = f"message successfully sent via pingme to {obfuscated}"
        response["body"] = json.dumps(data)
    except Exception as e:
        response["statusCode"] = 400
        response["body"] = e
        logging.error()

    return response

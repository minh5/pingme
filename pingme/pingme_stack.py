import os

from aws_cdk import core as cdk
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_events as events
import aws_cdk.aws_events_targets as targets



class PingmeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # lambda invocation via API`
        py_lambda = _lambda.Function(
            self,
            "handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="pingme.handler",
        )
        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=py_lambda,
        )

        # adding sns topics with SMS support
        phone_num = os.environ.get('PHONE_NUMBER')
        topic = sns.Topic(
            self,
            "SMS")
        sms_sub = subs.SmsSubscription(phone_num)
        topic.add_subscription(sms_sub)

        # hooking it up with eventbridge
        sms_target = targets.SnsTopic(topic)
        sms_pattern = events.EventPattern(detail=[{"source": ["aws.apigateway"]}])
        event_rule = events.Rule(
            self,
            "sms_rule",
            targets=[sms_target],
            event_pattern=sms_pattern
        )

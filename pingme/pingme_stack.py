import os

from aws_cdk import core as cdk
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
import aws_cdk.aws_events_targets as targets



class PingmeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # adding sns topics with SMS support
        phone_num = os.environ['PHONE_NUMBER']
        topic = sns.Topic(
            self,
            "SMS")
        sms_sub = subs.SmsSubscription(phone_num)
        topic.add_subscription(sms_sub)

        # creating the service role to be used
        sns_policy  = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess')
        lambda_policy = iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambda_FullAccess')
        service_role = iam.Role(self, 'pingme_svc_acct',
                                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))
        service_role.add_managed_policy(sns_policy)
        service_role.add_managed_policy(lambda_policy)

        # lambda invocation via API-Gateway
        py_lambda = _lambda.Function(
            self,
            "handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="pingme.handler",
            environment={
                'TOPIC_ARN': topic.topic_arn,
                'PHONE_NUMBER': phone_num
            },
            role=service_role
        )
        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=py_lambda,
        )

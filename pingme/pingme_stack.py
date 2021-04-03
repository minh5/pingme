from aws_cdk import core as cdk
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs



class PingmeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        py_lambda = _lambda.Function(
            self,
            "handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="handler",
        )
        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=py_lambda,
        )
        queue = sqs.Queue(
            self,
            "SMSQueue",
            visibility_timeout=cdk.Duration.seconds(300),
        )

        topic = sns.Topic(self, "SMS")
        topic.add_subscription(subs.SqsSubscription(queue))

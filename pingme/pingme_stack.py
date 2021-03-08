from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs

DEFAULT_ENV = {
    "CGO_ENABLED": "0",
    "GOOS": "darwin",
    "GOARCH": "amd64"}


class PingmeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        go_lambda = _lambda.Function(
            self,
            "handler",
            runtime=_lambda.Runtime.GO_1_X,
            code=_lambda.Code.from_asset(
                "lambda",
                bundling={
                    "image": _lambda.Runtime.GO_1_X.bundling_docker_image,
                    "user": "root",
                    "environment": DEFAULT_ENV,
                    "command": [
                        "bash",
                        "-c",
                        " && ".join(["make pingme", "make lambda-build"]),
                    ],
                }),
                handler="handler",
                environment=DEFAULT_ENV,
        )
        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=go_lambda,
        )
        queue = sqs.Queue(
            self,
            "SMSQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(self, "SMS")

        topic.add_subscription(subs.SqsSubscription(queue))

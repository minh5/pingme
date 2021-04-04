# pingme 

Simple app to ping me from the command line.

This project is to help me get better with CDK. The idea is to use API Gateway to trigger a lambda that will post to a topic to be consumed to send an SMS. The basic idea is like so:

```
pingme -> API Gateway -> Lambda -> SNS
```

To get started, first just set an environmental variable to post your number. Next you deploy this app to your AWS account via CDK. After deploying you will get an endpoint, you can make a POST request to the endpoint with the message and it will send to that to the SMS number. 

The workflow is generally like this.

```
# setting up
export PHONE_NUMBER=+11234567890
cdk deploy

pingme: deploying...
[0%] start: Publishing yourlambda:current
[100%] success: Published yourlambda:current
pingme: creating CloudFormation changeset...
[██████████████████████████▎·······························] (5/11)

 ✅  pingme

Outputs:
pingme.Endpoint8024A810 = https://<YOUR ENDPOINT>
```

Just take the endpoint provided and make a POST request

```
# making a request
curl https://<YOUR ENDPOINT> -d "hello world!"
```

## TODO

Set up either a `Makefile` or make some CLI helpers or as a python package.


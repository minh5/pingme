# pingme 

Simple app to ping me from the command line.

The idea is to use API Gateway to trigger a lambda that will post to a topic to be consumed to send an SMS. The basic idea is like so:

```
pingme -> API Gateway -> Lambda -> SNS
```

This project is to help me get better with CDK. 


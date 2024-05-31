# aws-connect-agent-event-processor

This demo solution uses a Lambda function to process records in an Amazon Kinesis data stream that has been configured to receive the Agent Events streaming from your Amazon Connect instance. The Kinesis event source mapping for the Lambda function uses `FilterCriteria` to filter agent events of `STATE_CHANGE` and sends out SMS/Email notifications if the agent status changed to any that is not equal to `Available`.

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, 

1. Copy the `samconfig.toml.tmpl` to `samconfig.toml` and update the following parameters:

```toml
parameter_overrides = [
    "ConnectInstanceArn=",
    "ConnectAgentEventsStreamArn=",
    "NotificationEmailAddr=",
    "NotificationPhoneNumber="
]
```

2. Run the following in your shell:

```bash
sam build
sam deploy
```

The first command will build the source of your application. The second command will package and deploy your application to AWS using the default configurations provided in the `samconfig.toml` file.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
sam build
```

The SAM CLI installs dependencies defined in `requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam local invoke ConnectAgentEventsFunction --event events/event.json
```

## Tests

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "aws-connect-agent-event-processor"
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

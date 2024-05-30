import json
import base64
import boto3
import os

agentStatusTopicArn = os.environ.get('agentStatus_SNS_TOPIC_ARN')
connectInstanceId = os.environ.get('agentStatus_SNS_TOPIC_ARN').split('/')[1]
connectClient = boto3.client('connect')
snsClient = boto3.client('sns')

def getConnectAgentByUserId(userId):
    try:
        response = connectClient.describe_user(
            InstanceId=connectInstanceId,
            UserId=userId
        )
        print(f"Agent details: {response}")
        agentName = response['User']['Username']
        return agentName
    
    except Exception as e:
        print(f"An error occurred {e}")
        raise e
    
def lambda_handler(event, context):

    # process records from Kinesis data stream
    for record in event['Records']:
        try:
            print(f"Processing agent event - EventID: {record['eventID']}")
            recordData = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            print(f"Record data: {recordData}")
            agentEvent = json.loads(recordData)
            print(f"Agent current status: {agentEvent['AgentARN']}, {agentEvent['CurrentAgentSnapshot']['AgentStatus']['Name']} at {agentEvent['CurrentAgentSnapshot']['AgentStatus']['StartTimestamp']}")
            agentId = agentEvent['AgentARN'].split('/')[-1]
            agentName = getConnectAgentByUserId(agentId)
            agentStatus = agentEvent['CurrentAgentSnapshot']['AgentStatus']['Name']
            if agentStatus != 'Available':
                print(f"Agent {agentName} changed status to {agentStatus}. Sending SMS notification.")
                snsResponse = snsClient.publish(
                    TopicArn=agentStatusTopicArn,
                    Message=f"Agent {agentName} changed status to ${agentStatus}."
                )
                print(f"SNS response: {snsResponse}")

        except Exception as e:
            print(f"An error occurred {e}")
            raise e
        
    print(f"Successfully processed {len(event['Records'])} records.")

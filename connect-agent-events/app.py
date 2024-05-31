import json
import base64
import boto3
import os
import pytz
from datetime import datetime, timezone

connectInstanceId = os.environ.get('AMAZON_CONNECT_INSTANCE_ARN').split('/')[1]
agentStatusTopicArn = os.environ.get('AGENT_STATUS_SNS_TOPIC_ARN')
connectClient = boto3.client('connect')
snsClient = boto3.client('sns')

def getConnectAgentByUserId(userId):
    try:
        
        #r = connectClient.list_users(
        #    InstanceId=connectInstanceId
        #)
        #print(f"Agent list: {r}")

        response = connectClient.describe_user(
            InstanceId=connectInstanceId,
            UserId=userId
        )
        print(f"Agent details: {response}")
        agentName = response['User']['Username']
        return agentName
    
    except Exception as e:
        print(f"An error occurred {e}")
        return f"Notfound: {userId}"
def getLocalTimestamp(timestampUtc):
    print(f"Timestamp UTC: {timestampUtc}")
    utc_datetime = datetime.strptime(timestampUtc, "%Y-%m-%dT%H:%M:%S.%fZ")
    singapore_tz = pytz.timezone("Asia/Singapore")
    local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=singapore_tz)
    return local_datetime.strftime('%Y-%m-%d %H:%M:%S SGT')

def lambda_handler(event, context):

    # process records from Kinesis data stream
    for record in event['Records']:
        try:
            print(f"Processing agent event - EventID: {record['eventID']}")
            recordData = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            print(f"Record data: {recordData}")
            agentEvent = json.loads(recordData)
            agentArn = agentEvent['AgentARN']
            agentId = agentArn.split('/')[-1]
            agentName = getConnectAgentByUserId(agentId)
            agentStatus = agentEvent['CurrentAgentSnapshot']['AgentStatus']['Name']
            startTimestamp = getLocalTimestamp(agentEvent['CurrentAgentSnapshot']['AgentStatus']['StartTimestamp'])
            print(f"Agent current status: {agentArn}, {agentName} changed status to {agentStatus} at {startTimestamp}")
            
            if agentStatus != 'Available':
                print(f"Agent '{agentName}' changed status to {agentStatus} at {startTimestamp}. Sending SMS notification.")
                snsResponse = snsClient.publish(
                    TopicArn=agentStatusTopicArn,
                    Message=f"Agent '{agentName}' changed status to ${agentStatus} at {startTimestamp}."
                )
                print(f"SNS response: {snsResponse}")

        except Exception as e:
            print(f"An error occurred {e}")
            raise e
        
    print(f"Successfully processed {len(event['Records'])} records.")

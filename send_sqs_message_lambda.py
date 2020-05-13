import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('sqs')

def lambda_handler(event, context):
    sqsUrls = event['sqs-subscribers']
    message_body = event['message-body']
    delay_seconds = 0
    if 'delay-seconds' in event:
        delay_seconds = event['delay-seconds']
    message_attributes = None
    if 'message-attributes' in event:
        message_attributes = event['message-attributes']
    message_deduplication_id = None
    if 'message-deduplication-id' in event:
        message_deduplication_id = event['message-deduplication-id']
    message_group_id = None
    if 'message-group-id' in event:
        message_group_id = event['message-group-id']
    
    failedAttempts = []
    
    for sqsUrl in sqsUrls:
        try:
            sendSQSMessage(
                sqsUrl, 
                message_body, 
                delay_seconds, 
                message_attributes,
                message_deduplication_id,
                message_group_id
                )
        except ClientError as e:
            failedAttempts.append({'sqsUrl': sqsUrl, 'error': e})
            
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Could not send all SQS messages!', 'failedAttempts': failedAttempts})
        
def sendSQSMessage(sqsUrl, 
                message_body, 
                delay_seconds, 
                message_attributes,
                message_deduplication_id,
                message_group_id):
    message = constructMessage(sqsUrl, 
                            message_body, 
                            delay_seconds, 
                            message_attributes,
                            message_deduplication_id,
                            message_group_id)
    client.send_message(**message)
    
def constructMessage(sqsUrl, 
                message_body, 
                delay_seconds, 
                message_attributes,
                message_deduplication_id,
                message_group_id):
    message = {
        'QueueUrl': sqsUrl,
        'MessageBody': message_body
    }
    if delay_seconds > 0:
        message.update({'DelaySeconds': delay_seconds})
    if message_attributes is not None:
        message.update({'MessageAttributes': message_attributes})
    if message_deduplication_id is not None:
        message.update({'MessageDeduplicationId': message_deduplication_id})
    if message_group_id is not None:
        message.update({'MessageGroupId': message_group_id})
    return message
    
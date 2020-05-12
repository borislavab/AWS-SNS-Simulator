import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    topic = event['topic']
    keyConditionExpr = f'partitionKeyName = {topic}'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SNS_Subscriptions')
    response = table.query(
        Select='COUNT',
        KeyConditionExpression=Key('topic').eq(topic)
    )
    count = response['Count']
    if count > 0:
        raise Exception({'errorMessage': 'Topic already exists!'})
    
    return table.put_item(
       Item={
            'topic': topic,
            'sqs_subscribers': [],
            'lambda_subscribers': [],
            'email_subscribers': [],
            'http_subscribers': []
        }
    )
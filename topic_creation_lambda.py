import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dummySubscriber = 'Dummy Subscriber'

def lambda_handler(event, context):
    topic = event['topic']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SNS_Subscriptions')
    
    item = {
        "topic": topic,
        "sqs_subscribers": set([dummySubscriber]),
        "lambda_subscribers": set([dummySubscriber]),
        "email_subscribers": set([dummySubscriber]),
        "http_subscribers": set([dummySubscriber])
    }
    conditionExpression = 'attribute_not_exists(topic)'

    try:
        return table.put_item(Item=item, ConditionExpression=conditionExpression)
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            raise Exception({'errorMessage': 'Topic already exists!'})
        else:
            raise
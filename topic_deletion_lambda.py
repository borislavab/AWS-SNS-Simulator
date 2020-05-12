import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    topic = event['topic']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SNS_Subscriptions')
    return table.delete_item(
        Key={
            'topic': topic
        }
    )
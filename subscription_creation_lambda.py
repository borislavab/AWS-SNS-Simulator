import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

allowedSubscriptionTypes = ['Email', 'SQS', 'Lambda', 'HTTP']
tableAttributesMap = {
    'Email': 'email_subscribers',
    'SQS': 'sqs_subscribers',
    'Lambda': 'lambda_subscribers',
    'HTTP': 'http_subscribers'
}

def lambda_handler(event, context):
    topic = event['topic']
    subscriptionType = event['subscriptionType']
    subscriberID = event['subscriberID']
    
    if subscriptionType not in allowedSubscriptionTypes:
        raise Exception({'errorMessage': 'Invalid subscription type!'})
    tableAttribute = tableAttributesMap[subscriptionType]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SNS_Subscriptions')
    updateExpression = f'ADD {tableAttribute} :elementSet'
    try:
        return table.update_item(
           Key={'topic': topic},
           UpdateExpression=updateExpression,
           ExpressionAttributeValues={":elementSet":set([subscriberID])},
           ConditionExpression=Key('topic').eq(topic)
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            raise Exception({'errorMessage': 'Topic does not exist!'})
        else:
            raise
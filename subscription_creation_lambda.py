import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

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
    projectionExpression=f'topic,{tableAttribute}'
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SNS_Subscriptions')
    response = table.get_item(
        Key={
            'topic': topic
        },
        ProjectionExpression=projectionExpression
    )
    if 'Item' not in response:
        raise Exception({'errorMessage': 'Topic does not exist!'})
    item = response['Item']
    attributeValues = item[tableAttribute]
    if subscriberID in attributeValues:
        return 'Subscription already exists'
    count = len(attributeValues)
    updateExpression = f'SET {tableAttribute}[{count}] = :insertValue'
    return table.update_item(
        Key={
            'topic': topic
        },
        UpdateExpression=updateExpression,
        ExpressionAttributeValues={
            ':insertValue': subscriberID
        }
    )
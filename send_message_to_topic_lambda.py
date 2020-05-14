import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SNS_Subscriptions')
lambda_client = boto3.client('lambda')

dummySubscriber = 'Dummy Subscriber'

def lambda_handler(event, context):
    topic = event['topic']
    parameters = event['parameters']
        
    response = table.get_item(
        Key={ 'topic': topic },
        ConsistentRead=True,
        ReturnConsumedCapacity='NONE'
    )
    
    if 'Item' not in response:
        raise Exception({'errorMessage': 'Topic does not exist!'})
        
    item = response['Item']
    email_subscribers = item['email_subscribers']
    sqs_subscribers = item['sqs_subscribers']
    lambda_subscribers = item['lambda_subscribers']
    
    email_subscribers.remove(dummySubscriber)
    sqs_subscribers.remove(dummySubscriber)
    lambda_subscribers.remove(dummySubscriber)
    
    failedAttempts = []
    
    invoke_message_sending_lambda(invoke_email_sending_lambda, failedAttempts, parameters, email_subscribers)
    invoke_message_sending_lambda(invoke_sqs_message_sending_lambda, failedAttempts, parameters, sqs_subscribers)
    invoke_message_sending_lambda(invoke_lambda_invoking_lambda, failedAttempts, parameters, lambda_subscribers)
    
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Some messages failed to deliver!', 'failedAttempts': failedAttempts})
        
def invoke_message_sending_lambda(message_sending_lambda, failedAttempts, parameters, subscribers):
    if len(subscribers) > 0:
        lambda_parameters = construct_lambda_parameters(parameters, subscribers)
        try:
            message_sending_lambda(lambda_parameters)
        except Exception as e:
            failedAttempts.append({'error': e})

def construct_lambda_parameters(parameters, subscribers):
    lambda_parameters = {'subscribers': list(subscribers)}
    lambda_parameters.update(parameters)
    return lambda_parameters
            
def invoke_email_sending_lambda(lambda_parameters):
    lambda_client.invoke(
        FunctionName='SNSSendEmail',
        InvocationType='Event',
        LogType='None',
        ClientContext='{}',
        Payload=json.dumps(lambda_parameters)
    )
    
def invoke_sqs_message_sending_lambda(lambda_parameters):
    lambda_client.invoke(
        FunctionName='SNSSendSQSMessage',
        InvocationType='Event',
        LogType='None',
        ClientContext='{}',
        Payload=json.dumps(lambda_parameters)
    )

def invoke_lambda_invoking_lambda(lambda_parameters):
    lambda_client.invoke(
        FunctionName='SNSInvokeLambdas',
        InvocationType='Event',
        LogType='None',
        ClientContext='{}',
        Payload=json.dumps(lambda_parameters)
    )
    
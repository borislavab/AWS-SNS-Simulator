import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    lambdas = event['lambda-subscribers']
    payload = None
    if 'payload' in event:
        payload = event['payload']
    context = None
    if 'context' in event:
        context = event['context']
    qualifier = None
    if 'qualifier' in event:
        qualifier = event['qualifier']
        
    failedAttempts = []
        
    for lambda_name in lambdas:
        try:
            invoke_lambda_async(lambda_name, payload, context, qualifier)
        except ClientError as e:
            failedAttempts.append({'lambda_name': lambda_name, 'error': e})
            
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Could not invoke all lambdas!', 'failedAttempts': failedAttempts})

def invoke_lambda_async(lambda_name, payload, context, qualifier):
    invocation = construct_invocation(lambda_name, payload, context, qualifier)
    client.invoke(**invocation)
    
def construct_invocation(lambda_name, payload, context, qualifier):
    invocation = {
        'FunctionName': lambda_name,
        'InvocationType': 'Event',
        'LogType': 'None'
    }
    if context is not None:
        invocation.update({'ClientContext': context})
    if payload is not None:
        invocation.update({'Payload': payload})
    if qualifier is not None:
        invocation.update({'Qualifier': qualifier})
    return invocation

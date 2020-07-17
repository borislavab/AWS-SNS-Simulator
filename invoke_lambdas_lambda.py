import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    lambdas = event['subscribers']
    payload = event['message']
    if 'payload' in event:
        payload = event['payload']
    client_context = None
    if 'client-context' in event:
        client_context = event['client-context']
    qualifier = None
    if 'qualifier' in event:
        qualifier = event['qualifier']
        
    failedAttempts = []
        
    for lambda_name in lambdas:
        try:
            invoke_lambda_async(lambda_name, payload, client_context, qualifier)
        except ClientError as e:
            failedAttempts.append({'lambda_name': lambda_name, 'error': e})
            
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Could not invoke all lambdas!', 'failedAttempts': failedAttempts})

def invoke_lambda_async(lambda_name, payload, client_context, qualifier):
    invocation = construct_invocation(lambda_name, payload, client_context, qualifier)
    client.invoke(**invocation)
    
def construct_invocation(lambda_name, payload, client_context, qualifier):
    invocation = {
        'FunctionName': lambda_name,
        'InvocationType': 'Event',
        'LogType': 'None'
    }
    if client_context is not None:
        invocation.update({'ClientContext': client_context})
    if payload is not None:
        invocation.update({'Payload': json.dumps(payload)})
    if qualifier is not None:
        invocation.update({'Qualifier': qualifier})
    return invocation

import json
import boto3
from botocore.exceptions import ClientError
import os

charset = 'UTF-8'
email_server_region = os.environ['EMAIL_SERVER_REGION']
sender = os.environ['EMAIL_SENDER']
sender_access_key = os.environ['SENDER_ACCESS_KEY']
sender_secret_access_key = os.environ['SENDER_SECRET_ACCESS_KEY']

def lambda_handler(event, context):
    recipientList = event['subscribers']
    subject = event['subject']
    body_text = None
    if 'body-text' in event:
        body_text = event['body-text']
    body_html = None
    if 'body-html' in event:
        body_html = event['body-html']
    message = constructMessage(subject, body_text, body_html)
    client = boto3.client('ses',
                            region_name=email_server_region, 
                            aws_access_key_id=sender_access_key,
                            aws_secret_access_key=sender_secret_access_key)
    failedAttempts = []
    
    for recipient in recipientList:
        try:
            sendEmailToRecipient(client, recipient, message)
        except ClientError as e:
            failedAttempts.append({'recipient': recipient, 'error': e})
            
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Could not send all emails!', 'failedAttempts': failedAttempts})
    
def sendEmailToRecipient(client, recipient, message):
    client.send_email(
        Destination={
            'ToAddresses': [
                recipient,
            ],
        },
        Message=message,
        Source=sender
    )
    
def constructMessage(subject, body_text, body_html):
    body = constructBody(body_text, body_html)
    subject_data = construct_data(subject)
    return {
            'Body': body,
            'Subject': subject_data,
        }

def constructBody(body_text, body_html):
    body = {}
    if body_html is not None:
        html_body = construct_data(body_html)
        body.update({'Html': html_body})
    if body_text is not None:
        text_body = construct_data(body_text)
        body.update({'Text': text_body})
    if body == {}:
        raise Exception({'errorMessage': 'No body passed'})
    return body

def construct_data(data):
    return {
        'Charset': charset,
        'Data': data
    }
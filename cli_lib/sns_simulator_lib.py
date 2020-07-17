import json
import boto3

class InvalidSubscriptionType(Exception):
    pass

class SNSSimulatorLib:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token):
        self.lambda_client = boto3.client('lambda',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        self.subscription_types = ['Email', 'SQS', 'Lambda', 'HTTP']

    def send_message(self, topic, parameters):
        lambda_params = {
            'topic': topic,
            'parameters': parameters
        }
        self.invoke_lambda('SendMessageToSNSTopic', lambda_params)

    def create_topic(self, topic):
        lambda_params = {
            'topic': topic
        }
        self.invoke_lambda('CreateSNSTopic', lambda_params)

    def delete_topic(self, topic):
        lambda_params = {
            'topic': topic
        }
        self.invoke_lambda('DeleteSNSTopic', lambda_params)

    def subscribe_to_topic(self, topic, subscription_type, subscriber_id):
        if subscription_type not in self.subscription_types:
            raise InvalidSubscriptionType(f'invalid subscription type {subscription_type}')

        lambda_params = {
            'topic': topic,
            'subscriptionType': subscription_type,
            'subscriberID': subscriber_id
        }
        self.invoke_lambda('SubscribeToSNSTopic', lambda_params)

    def unsubscribe_from_topic(self, topic, subscription_type, subscriber_id):
        if subscription_type not in self.subscription_types:
            raise InvalidSubscriptionType(f'invalid subscription type {subscription_type}')

        lambda_params = {
            'topic': topic,
            'subscriptionType': subscription_type,
            'subscriberID': subscriber_id
        }
        self.invoke_lambda('UnsubscribeFromSNSTopic', lambda_params)

    # def invoke_lambda(self, *kwargs):
    #     print(*kwargs)

    def invoke_lambda(self, lambda_name, lambda_parameters):
        self.lambda_client.invoke(
            FunctionName=lambda_name,
            InvocationType='Event',
            LogType='None',
            ClientContext='{}',
            Payload=json.dumps(lambda_parameters)
        )

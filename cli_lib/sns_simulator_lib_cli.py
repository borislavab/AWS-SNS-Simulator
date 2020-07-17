import argparse
import sys
import textwrap
import json
import configparser

import sns_simulator_lib

class CliClient:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Custom SNS client',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=textwrap.dedent('''\
            %(prog)s <command> [<args>]\n

                send-message    Use to send message to topic
                create-topic    Use to create topic
                delete-topic    Use to delete topic
                subscribe       Use to subscribe to topic
                unsubscribe     Use to subscribe from topic
            '''))

        parser.add_argument('command', help='Subcomand to run')

        args = parser.parse_args(sys.argv[1:2])
        command = args.command.replace('-', '_')
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.sns_client = sns_simulator_lib.SNSSimulatorLib(
            region_name='us-east-1',
            aws_access_key_id=config['default']['aws_access_key_id'],
            aws_secret_access_key=config['default']['aws_secret_access_key'],
            aws_session_token=config['default']['aws_session_token'])
        getattr(self, command)()

    def send_message(self):
        parser = argparse.ArgumentParser(description='Use to send message to topic')
        parser.add_argument('--topic', action='store', required=True)
        parser.add_argument('--message', action='store', required=True)
        parser.add_argument('--message-type', action='store', default='text', choices=['text', 'path-to-file', 'path-to-json'])
        args = parser.parse_args(sys.argv[2:])
        if args.message_type == 'text':
            msg = {
                'message': args.message
            }
            self.sns_client.send_message(args.topic, msg)
        elif args.message_type == 'path-to-file':
            file = open(args.message).read()
            msg = {
                'message': file
            }
            self.sns_client.send_message(args.topic, msg)
        else:
            file = open(args.message).read()
            self.sns_client.send_message(args.topic, json.loads(file))


    def create_topic(self):
        parser = argparse.ArgumentParser(description='Use to create topic')
        parser.add_argument('--topic', action='store', required=True)
        args = parser.parse_args(sys.argv[2:])
        self.sns_client.create_topic(args.topic)

    def delete_topic(self):
        parser = argparse.ArgumentParser(description='Use to delete topic')
        parser.add_argument('--topic', action='store', required=True)
        args = parser.parse_args(sys.argv[2:])
        self.sns_client.delete_topic(args.topic)

    def subscribe(self):
        subscription_types = self.sns_client.subscription_types
        parser = argparse.ArgumentParser(description='Use to subscribe to topic')
        parser.add_argument('--topic', action='store', required=True)
        parser.add_argument('--subscription-type', action='store', choices=subscription_types, required=True)
        parser.add_argument('--subscriber-id', action='store', required=True)
        args = parser.parse_args(sys.argv[2:])
        self.sns_client.subscribe_to_topic(args.topic, args.subscription_type, args.subscriber_id)

    def unsubscribe(self):
        subscription_types = self.sns_client.subscription_types
        parser = argparse.ArgumentParser(description='Use to unsubscribe from topic')
        parser.add_argument('--topic', action='store', required=True)
        parser.add_argument('--subscription-type', action='store', choices=subscription_types, required=True)
        parser.add_argument('--subscriber-id', action='store', required=True)
        args = parser.parse_args(sys.argv[2:])
        self.sns_client.unsubscribe_from_topic(args.topic, args.subscription_type, args.subscriber_id)

def main():
    CliClient()

if __name__ == '__main__':
    main()

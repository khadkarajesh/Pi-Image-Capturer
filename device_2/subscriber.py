import argparse
import time
import json
from google.cloud import pubsub_v1
import os

# TODO Path to google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


def callback(message):
    os.system("open \"\" {}".format(message.data))
    print('Received message: {}'.format(message))
    message.ack()


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Example Google Cloud IoT MQTT device connection code.')
    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        required=True,
        help='GCP cloud project name.')
    parser.add_argument(
        '--subscription_name', required=True, help='Cloud IoT Topic name')
    return parser.parse_args()


def main():
    args = parse_command_line_args()
    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        args.project_id, args.subscription_name)

    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()

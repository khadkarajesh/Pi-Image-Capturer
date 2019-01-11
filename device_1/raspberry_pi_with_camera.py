import argparse
import datetime
import os
import time
import socket
import random
from random import randint
import json
import sys
import jwt
import paho.mqtt.client as mqtt
from camera import Camera
from google.cloud import storage
from pprint import pprint

def publish_messages(project_id, topic_name, url):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.publish(topic_path, url)
    print("published data")
    
    
def create_topic(project_id, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    topic = publisher.create_topic(topic_path)
    print('Topic created: {}'.format(topic))
    
def list_topics(project_id):
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project_id)
    for topic in publisher.list_topics(project_path):
        print(topic)             

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    #print('on_publish')
    

def on_message(unused_client, unused_userdata, message):
        """Callback when the device receives a message on a subscription."""
        payload = message.payload
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))
        print(payload.decode('utf-8'))
        if payload.decode('utf-8') == 'on':
            to_save_image_path = sys.path[0] + '/'    
            preview_capture(to_save_image_path)
            # TODO Replace with you bucket name
            bucket_name = 'demo-iot'
            url = upload_file(to_save_image_path,bucket_name)
            print(url)
            # rasp3: replace with your device name in your registry
            mqtt_event = '/devices/{}/events'.format(args.device_id)
            unused_client.publish(mqtt_event, url, qos=1)
        else:
            print('off')

def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                       .format(
                               project_id,
                               cloud_region,
                               registry_id,
                               device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    
    return client

def subscribe_command_with(client, device_id):
    mqtt_command = '/devices/{}/commands/#'.format(device_id)
    client.subscribe(mqtt_command)

def subscribe_event_with(client, device_id):
    mqtt_event = '/devices/{}/events'.format(device_id)
    client.subscribe(mqtt_event)
    
def get_camera():
    camera = Camera()
    return camera

def preview_capture(path):
    camera = get_camera()
    camera.start_preview()
    time.sleep(5)
    camera.capture(path)
    camera.stop_preview()
    camera.close_camera()
    
    
          
def upload_file(path, bucket_name):
    storage_client = storage.Client()
    pprint(bucket_name)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('image/')
    blob.upload_from_filename(path)
    return blob.public_url

def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
            '--project_id',
            default=os.environ.get('GOOGLE_CLOUD_PROJECT'),
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument(
            '--device_id', required=True, help='Cloud IoT Core device id')
    parser.add_argument(
            '--private_key_file',
            required=True, help='Path to private key file.')
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            default='RS256',
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--ca_certs',
            default='roots.pem',
            help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
            '--mqtt_bridge_hostname',
            default='mqtt.googleapis.com',
            help='MQTT bridge hostname.')
    parser.add_argument(
            '--mqtt_bridge_port',
            choices=(8883, 443),
            default=8883,
            type=int,
            help='MQTT bridge port.')
    parser.add_argument('--bucket', required=True)
    return parser.parse_args()


# [START iot_mqtt_run]
def main():
    args = parse_command_line_args()
    client = get_client(
        args.project_id, args.cloud_region, args.registry_id, args.device_id,
        args.private_key_file, args.algorithm, args.ca_certs,
        args.mqtt_bridge_hostname, args.mqtt_bridge_port)
    subscribe_command_with(client, args.device_id)  
    # Start the network loop.
    client.loop_forever()
    #time.sleep(5)
    print('Finished.')
# [END iot_mqtt_run]


if __name__ == '__main__':
    main()

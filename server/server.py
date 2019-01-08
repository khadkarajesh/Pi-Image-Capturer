#!/usr/bin/env python

import argparse
import base64
import io
import os
import sys
import time

from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)


def send_command(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        command):
    """Send a command to a device."""
    # [START iot_send_command]
    print('Sending command to device')
    client = get_client(service_account_json)
    device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id, cloud_region, registry_id, device_id)

    config_body = {
        'binaryData': base64.urlsafe_b64encode(
            command.encode('utf-8')).decode('ascii')
    }

    return client.projects(
    ).locations().registries(
    ).devices().sendCommandToDevice(
        name=device_path, body=config_body).execute()
    # [END iot_send_command]


def parse_command_line_args():
    """Parse command line arguments."""
    default_registry = 'cloudiot_device_manager_example_registry_{}'.format(
        int(time.time()))

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Optional arguments
    parser.add_argument(
        '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
        '--pubsub_topic',
        help=('Google Cloud Pub/Sub topic. '
              'Format is projects/project_id/topics/topic-id'))
    parser.add_argument(
        '--device_id',
        default=None,
        help='Device id.')
    parser.add_argument(
        '--ec_public_key_file',
        default=None,
        help='Path to public ES256 key file.')
    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help='GCP cloud project name.')
    parser.add_argument(
        '--registry_id',
        default=default_registry,
        help='Registry id. If not set, a name will be generated.')
    parser.add_argument(
        '--rsa_certificate_file',
        default=None,
        help='Path to RS256 certificate file.')
    parser.add_argument(
        '--service_account_json',
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help='Path to service account json file.')
    parser.add_argument('--command', help='send commands to device')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line_args()
    send_command(args.service_account_json, args.project_id,
                 args.cloud_region, args.registry_id, args.device_id, args.command)

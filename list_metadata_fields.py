#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""list_metadata_fields.py
"""

import csv
import gzip
import time
import shutil
import urllib.request

from pathlib import Path
from os import environ as env
from dotenv import load_dotenv

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

import constants


def walk_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_keys(v, path + "." + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            s = "[" + str(i) + "]"
            yield from walk_keys(v, path + s if path else s)
    else:
        yield path


def connect_to_auth0():
    """Connect to Auth0 using Client Credentials flow. Credentials are stored
    in .env"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    auth0_client_id = env[constants.AUTH0_CLIENT_ID]
    auth0_client_secret = env[constants.AUTH0_CLIENT_SECRET]
    auth0_domain = env[constants.AUTH0_DOMAIN]
    mgmt_api_url = 'https://'+auth0_domain+'/api/v2/'

    get_token = GetToken(auth0_domain)
    token = get_token.client_credentials(auth0_client_id,
                                         auth0_client_secret,
                                         mgmt_api_url)
    mgmt_api_token = token['access_token']
    return Auth0(auth0_domain, mgmt_api_token)


def main():
    """main"""

    auth0 = connect_to_auth0()

    export_job = {}
    export_job_id = auth0.jobs.export_users(export_job)['id']

    while auth0.jobs.get(export_job_id)['status'] != 'completed':
        time.sleep(5)

    export_job_output_dir = './output'
    export_job_output_gz_filename = 'export.csv.gz'
    export_job_output_gz_filepath = (export_job_output_dir +
                                     '/' + export_job_output_gz_filename)
    urllib.request.urlretrieve(auth0.jobs.get(export_job_id)['location'],
                               export_job_output_gz_filepath)

    export_job_output_csv_filename = 'export.csv'
    export_job_output_csv_filepath = (export_job_output_dir +
                                      '/' + export_job_output_csv_filename)
    with gzip.open(export_job_output_gz_filepath, 'rb') as gz_file:
        with open(export_job_output_csv_filepath, 'wb') as csv_file:
            shutil.copyfileobj(gz_file, csv_file)

    users = []

    with open(export_job_output_csv_filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for user in csv_reader:
            users.append(auth0.users.get(user[0],
                                         fields=['user_metadata',
                                                 'app_metadata'],
                                         include_fields=True))
            time.sleep(1)

    for s in sorted(walk_keys(users)):
        print(s)


if __name__ == '__main__':
    main()

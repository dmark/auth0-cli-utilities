#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""getcxnid.py"""


import argparse

from pathlib import Path
from os import environ as env
from dotenv import load_dotenv

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

import constants


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


def get_args():
    """Processes command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connection', required=True,
                        help='Name of the connection.')
    return parser.parse_args()


def main():
    """main"""
    args = get_args()
    auth0 = connect_to_auth0()

    connections = auth0.connections.all()
    for connection in connections:
        if connection['name'] == args.connection:
            print(connection['id'])


if __name__ == '__main__':
    main()

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""getuser.py"""


import json
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
    parser = argparse.ArgumentParser(description='Dumps one specifed user ' +
                                     'or all users as JSON.')
    parser.add_argument('-c', '--connection')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--user_id',
                       help='Search by Auth0 user_id attribute.')
    group.add_argument('-e', '--email',
                       help='Search by email address.')
    group.add_argument('-u', '--username',
                       help='Search by username.')
    return parser.parse_args()


def main():
    """main"""
    args = get_args()
    auth0 = connect_to_auth0()

    if args.user_id:
        print(json.dumps(auth0.users.get(args.user_id),
                         sort_keys=True, indent=4, separators=(',', ':')))

    elif args.email:
        pass

    elif args.username:
        pass

    else:
        print(args.print_help())


if __name__ == '__main__':
    main()

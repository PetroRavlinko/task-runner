#!/usr/bin/python
import os
import argparse

S3_HISTORY_BUCKET_NAME_ENV = 'S3_HISTORY_BUCKET_NAME_ENV'
S3_ENDPOINT_URL_ENV = 'S3_ENDPOINT_URL'

class Context():
    def __init__(self):
        self.s3_history_bucket_name = os.getenv(S3_HISTORY_BUCKET_NAME_ENV, 'bucket')
        self.s3_endpoint_url = os.getenv(S3_ENDPOINT_URL_ENV, '{}://{}:{}'.format('http', 'localhost', '4566'))

        self.parser = argparse.ArgumentParser(prog='eat', description='Automated Task Executor (ATE). Run automated custom steps.')
        self.define_arguments()                                
    
    def define_arguments(self) -> None:
        self.parser.add_argument('-a',
                            dest='accountType',
                            default='dev',
                            metavar='ACCOUNT_TYPE',
                            type=str,
                            help='Account type')
        self.parser.add_argument('-p',
                            dest='awsCliProfile',
                            default='default',
                            metavar='PROFILE',
                            type=str,
                            help='aws-cli profile')
        self.parser.add_argument('--region',
                            dest='awsRegion',
                            default='us-west-1',
                            metavar='REGION',
                            type=str,
                            help='AWS region')


    def get_arguments(self):
        return self.parser.parse_args()

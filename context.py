#!/usr/bin/python
import argparse

class Context():
    def __init__(self):
        self.s3_endpoint_url = '{}://{}:{}'.format('http', 'localhost', '4566')
        self.task_run_history_s3_bucket_name = 'bucket'
        self.parser = argparse.ArgumentParser(prog='eat',
                                        description='Automated Task Executor (ATE). Run automated custom steps.')
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
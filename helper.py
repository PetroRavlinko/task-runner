#!/usr/bin/python
import os
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(prog='eat',
                                     description='Automated Task Executor (ATE). Run automated custom steps.')
    parser.add_argument('-a',
                        dest='accountType',
                        default='dev',
                        metavar='ACCOUNT_TYPE',
                        type=str,
                        help='Account type')
    parser.add_argument('-p',
                        dest='awsCliProfile',
                        default='default',
                        metavar='PROFILE',
                        type=str,
                        help='aws-cli profile')
    parser.add_argument('--region',
                        dest='awsRegion',
                        default='us-west-1',
                        metavar='REGION',
                        type=str,
                        help='AWS region')

    return parser.parse_args()

class Task(object):
    def __init__(self, context):
        self.context = context
        self.subtasks = []

    def __str__(self):
        return f'Task: {os.path.basename(__file__)}'

    def add_subtask(self, task):
        self.subtasks.append(task)


if __name__ == '__main__':
    print(Task({}))

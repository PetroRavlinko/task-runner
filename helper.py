#!/usr/bin/python
import os
import subprocess
import argparse
import fnmatch


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


def execute_tasks():
    executed_tasks = []
    try:
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*-[0-9]*.py'):
                print(file)
                result = subprocess.run(["python", file], stdout=subprocess.PIPE)
                print(result.stdout.decode('utf-8'))
                executed_tasks.append(file)
    except StepException:
        for file in executed_tasks:
            subprocess.run(["python", file, '--rollback'], stdout=subprocess.PIPE).stdout.decode('utf-8')


class StepException(Exception):
    pass


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

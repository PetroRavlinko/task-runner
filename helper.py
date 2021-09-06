#!/usr/bin/python
import os
import subprocess
import argparse
import fnmatch
import json
import time


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


executing_results = []


def execute_tasks():
    executed_tasks = []
    for file in os.listdir('.'):
        task_execution_result = {}

        if fnmatch.fnmatch(file, '*_[0-9]*.py'):
            print(file)
            task_execution_result.update({'file': file})

            result = subprocess.run(['python', file], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))
            executed_tasks.append(file)
            executing_results.append(task_execution_result)

    json_object = json.dumps(executing_results, indent=4)
    time_str = time.strftime("%Y%m%d-%H%M%S")
    with open(f"execution_{time_str}.json", "w") as outfile:
        outfile.write(json_object)


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

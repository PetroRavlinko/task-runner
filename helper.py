#!/usr/bin/python
import os
import subprocess
import argparse
import fnmatch
import json
import time
import datetime
import hashlib

from enum import Enum


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


def plan_tasks():
    tasks = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*_[0-9]*.py'):
            task = Task(file)
            tasks.append(task)
    return tasks


def task_json_converter(o):
    if isinstance(o, TaskEvent):
        return o.__dict__
    if isinstance(o, datetime.datetime):
        return str(o)


def execute_tasks():
    for task in plan_tasks():
        task.run()
        print(json.dumps(task.__dict__, default=task_json_converter))

    # json_object = json.dumps(executing_results, indent=4)
    # time_str = time.strftime("%Y%m%d-%H%M%S")

    # with open(f"execution_{time_str}.json", "w") as outfile:
        # outfile.write(json_object)


def print_task_stdout(argument):
    def decorator(func):
        def wrapper(file):
            print(file)
            result = func(file)
            print(result.stdout.decode('utf-8'))
            print(result)
        return wrapper
    return decorator


class StepException(Exception):
    pass


def rollback_on_fail(func):
    def wrapper(self):
        result = func(self)
        print(result)
        if result.returncode != 0:
            self.failed()
            result = self.rollback()
    return wrapper


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Task(object):
    def __init__(self, file):
        self.file = file
        self.status = 'CREATED'
        self.md5 = md5(file)
        self.datetime = datetime.datetime.now()
        self.stdout = 'Task is created'
        self.actions = []

    @rollback_on_fail
    def run(self):
        self.status = 'IN_PROGRESS'
        result = subprocess.run(['python', self.file], stdout=subprocess.PIPE)
        self.stdout = result.stdout.decode('utf-8')
        self.track_event()
        return result


    def rollback(self):
        result = subprocess.run(
            ['python', self.file, '--rollback'],
            stdout=subprocess.PIPE)
        self.stdout = result.stdout.decode('utf-8')
        print(result)
        if result.returncode == 0:
            self.status = 'ROLLED_BACK'
        else:
            self.status = 'ROLLBACK_FAILED'
        self.track_event()
        return result

    def failed(self):
        self.status = 'FAILED'
        self.stdout = 'Task is failed'
        self.track_event()

    def track_event(self):
        self.actions.append(TaskEvent(self))


class TaskEvent(object):
    def __init__(self, task):
        self.datetime = datetime.datetime.now()
        self.status = task.status
        self.stdout = task.stdout

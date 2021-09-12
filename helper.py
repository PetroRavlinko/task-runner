#!/usr/bin/python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import os
import subprocess
import fnmatch
import json
import time
import datetime
import hashlib
import logging
import boto3
from enum import Enum

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level = logging.INFO)


class TaskEvent(object):
    def __init__(self, task):
        self.taskName = task.file
        self.datetime = datetime.datetime.now()
        self.status = task.status
        self.stdout = task.stdout


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class TaskEventSubject(Subject):
    _state: TaskEvent = None

    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def trace(self, taskEvent: TaskEvent) -> None:
        self._state = taskEvent
        self.notify()


class TaskEventConsoleOutObserver(Observer):
    def update(self, subject: Subject) -> None:
        logging.info(f"{subject._state.taskName} - {subject._state.status} - {subject._state.stdout}")



def plan_tasks():
    tasks = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*_[0-9]*.py'):
            task = Task(file)
            tasks.append(task)
    return tasks


def task_json_converter(o):
    if isinstance(o, Task):
        return o.__dict__
    if isinstance(o, TaskEvent):
        return o.__dict__
    if isinstance(o, datetime.datetime):
        return str(o)
    if isinstance(o, TaskStatus):
        return o.name


save_to_file = True
eventSubject = TaskEventSubject()
consoleOutObserver = TaskEventConsoleOutObserver()
eventSubject.attach(consoleOutObserver)
s3bucketName = 'bucket'
endpoint_url = os.getenv('S3_ENDPOINT_URL', '{}://{}:{}'.format('http', 'localhost', '4566'))

if endpoint_url:
    s3 = boto3.client('s3', endpoint_url=endpoint_url, verify=False)
else:
    s3 = boto3.client('s3')

def saveToJsonFile(tasks: List[Task]) -> str:
    json_object = json.dumps(tasks, default=task_json_converter)
    time_str = time.strftime("%Y%m%d-%H%M%S")
    json_file_name = f"execution_{time_str}.json"

    with open(json_file_name, "w") as outfile:
        outfile.write(json_object)
    
    return json_file_name
    
def safeOnS3(file_name: str) -> None:
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, s3bucketName, file_name)

def save_on_s3(func):
    def wrapper():
        tasks = func()

        if save_to_file:
            safeOnS3(saveToJsonFile(tasks))
    
    return wrapper


@save_on_s3
def execute_tasks():
    tasks = []

    for task in plan_tasks():
        task.run()
        tasks.append(task)
    
    return task


def rollback_on_fail(func):
    def wrapper(self):
        result = func(self)
        if result.returncode != 0:
            self.failed()
            self.rollback()

    return wrapper


def sha256(fname):
    with open(fname, "rb") as f:
        chunk = f.read()
        readable_hash = hashlib.sha256(chunk)
    return readable_hash.hexdigest()

class TaskStatus(Enum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    ROLLED_BACK = 'ROLLED_BACK'
    ROLLBACK_FAILED = 'ROLLBACK_FAILED'
    FAILED = 'FAILED'


class Task(object):
    def __init__(self, file):
        self.file = file
        self.status = TaskStatus.CREATED
        self.sha256 = sha256(file)
        self.datetime = datetime.datetime.now()
        self.stdout = 'Task is created'
        self.actions = []

    @rollback_on_fail
    def run(self):
        self.status = TaskStatus.IN_PROGRESS
        result = subprocess.run(['python', self.file], stdout=subprocess.PIPE)
        self.stdout = result.stdout.decode('utf-8')
        self.track_event()
        return result

    def rollback(self):
        result = subprocess.run(
            ['python', self.file, '--rollback'], stdout=subprocess.PIPE)
        self.stdout = result.stdout.decode('utf-8')
        if result.returncode == 0:
            self.status = TaskStatus.ROLLED_BACK
        else:
            self.status = TaskStatus.ROLLBACK_FAILED
        self.track_event()
        return result

    def failed(self):
        self.status = TaskStatus.FAILED
        self.stdout = 'Task is failed'
        self.track_event()

    def track_event(self):
        taskEvent: TaskEvent = TaskEvent(self)
        self.actions.append(taskEvent)
        eventSubject.trace(taskEvent)

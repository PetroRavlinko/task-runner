#!/usr/bin/pythonsys.argv
import sys


def execute():
    print("Task is running...")


def rollback():
    print('Rollback is running...')


if __name__ == '__main__':
    if sys.argv.__contains__('--rollback'):
        rollback()
    else:
        execute()


#!/usr/bin/pythonsys.argv
import sys


def execute():
    try:
        print("Task is running...")
        raise Exception('Some issue')
    except Exception:
        exit(1)


def rollback():
    print('Rollback is running...')


if __name__ == '__main__':
    if sys.argv.__contains__('--rollback'):
        rollback()
    else:
        execute()

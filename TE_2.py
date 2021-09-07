#!/usr/bin/pythonsys.argv
import sys
import helper


def init():
    print('Hi')  # Press ⌘F8 to toggle the breakpoint.


def execute():
    try:
        print("Task is running...")
        raise helper.StepException('Some issue')
    except helper.StepException:
        exit(1)


def rollback():
    print('Rollback is running...')


if __name__ == '__main__':
    if sys.argv.__contains__('--rollback'):
        rollback()
    else:
        execute()

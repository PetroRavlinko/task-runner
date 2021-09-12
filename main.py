#!/usr/bin/python
from helper import TaskRunner
from context import Context



def main():
    context = Context()
    args = context.get_arguments()
    print(args.accountType)
    print(args.awsCliProfile)
    print(args.awsRegion)
    task_runner = TaskRunner(context)
    task_runner.execute_tasks()


if __name__ == '__main__':
    main()

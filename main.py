#!/usr/bin/python
import helper
from context import Context



def main():
    context = Context()
    args = context.get_arguments()
    print(args.accountType)
    print(args.awsCliProfile)
    print(args.awsRegion)
    helper.execute_tasks()


if __name__ == '__main__':
    main()

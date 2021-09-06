#!/usr/bin/python
import helper


def main():
    args = helper.get_arguments()
    print(args.accountType)
    print(args.awsCliProfile)
    print(args.awsRegion)
    helper.execute_tasks()


if __name__ == '__main__':
    main()

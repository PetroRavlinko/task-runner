#!/usr/bin/python
import os
import fnmatch
import helper


def main():
    args = helper.get_arguments()
    print(args.accountType)
    print(args.awsCliProfile)
    print(args.awsRegion)
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*-[0-9]*.py'):
            print(file)
            os.system(f"python {file} --rollback")


if __name__ == '__main__':
    main()

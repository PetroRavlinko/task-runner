#!/usr/bin/python
import boto3

from context import Context

class S3Adapter(object):
    def __init__(self, context: Context):
        self.endpoint_url = context.s3_endpoint_url
        if context.s3_endpoint_url:
            self.s3 = boto3.client('s3', endpoint_url=context.s3_endpoint_url, verify=False)
        else:
            self.s3 = boto3.client('s3')

def saveobj_on_s3(s3_bucket_name):
    def decorator(func):
        def wrapper(self):
            filename = func(self)
            s3_adapter = S3Adapter(self.context)
            with open(filename, "rb") as f:
                s3_adapter.s3.upload_fileobj(f, s3_bucket_name, filename)
        return wrapper
    return decorator

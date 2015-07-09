# -*- coding: utf-8 -*-
"""!aws <aws command> returns the output of aws command"""

import boto3
import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!aws (.*)", text)
    if not match:
        return
    s3 = boto3.resource('s3')
    name = []
    for bucket in s3.buckets.all():
        name.append(bucket.name)
    return "\n".join(name)
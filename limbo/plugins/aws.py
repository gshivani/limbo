# -*- coding: utf-8 -*-
"""!aws <aws command> returns the output of aws command"""

import boto3
import re

def on_message(msg, server):
    text = msg.get("text", "")
    instance_id = []
    instance_tag = []
    ec2 = boto3.resource('ec2')
    if re.findall(r"!aws server count", text):
        instances = ec2.instances.all()
        for instance in instances:
            instance_id.append(instance.id)
        return "There are "+ str(len(instance_id)) + " servers"
    elif re.findall(r"!aws server running count", text):
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            instance_id.append(instance.id)
        return "There are " + str(len(instance_id)) + " servers running right now"
    elif re.findall(r"!aws server count for (.*)", text):
        #tag = match[0]
        instances = ec2.instances.filter(
            Filters=[{'Name': 'tag-value', 'Values': ['nroute']}])
        for instance in instances:
            instance_id.append(instance.id)
        return "There are " + str(len(instance_id)) + " servers with tag" + tag
    else:
        return
    
    
    #s3 = boto3.resource('s3')
    #name = []
    #for bucket in s3.buckets.all():
        #name.append(bucket.name)
    #n = len(name)
    #return "There are " + str(n) + " servers running"
    #return "\n".join(name)
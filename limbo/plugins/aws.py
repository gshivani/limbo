# -*- coding: utf-8 -*-
"""!aws <command> returns information on ec2 instances based on given command"""

import boto3
import re
from datetime import date, timedelta

STATES = ['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']
ec2 = boto3.resource('ec2')

def on_message(msg, server):
    text = msg.get("text", "")
    ec2 = boto3.resource('ec2')
    instance_id = []

    # Extract various features of the text
    tag      = re.findall(r"^!aws.*tag (.*)$", text)
    state    = re.findall(r"^!aws.*state (.*)$", text)
    age      = re.findall(r"^!aws.*older than (.*) days$", text)
    instance = re.findall(r"^!aws.*instance (.*)$", text)
    
    if tag:
        pattern = re.compile('.*:.*')
        if pattern.match(tag[0]) is None:
            return "ERROR: Tag must be in key:value format. Ex: (role:nroute)"

    if state:
        if state[0].encode("utf8") not in STATES:
            return "ERROR: State must be one of: {}".format(", ".join(STATES))

    if age:
        pattern = re.compile('\d+')
        if pattern.match(age[0]) is None:
            return "ERROR: Age must be a numeric in days. Ex: (age 5)"

    if instance:
        pattern = re.compile('i-.*')
        if pattern.match(instance[0]) is None:
            return "ERROR: instance format is i-23482221. Ex: (instance i-23482221)"


    # Counting servers
    if re.match(r"^!aws count server.*$", text):
        if state:
            return _count(state=state[0].encode("utf8"))
        elif tag:
            return _count(tag=tag[0])
        else:
            return _count()

    # Details of servers
    if re.match(r"^!aws details.*$", text):
        if tag:
            return _details(tag=tag[0])
        elif age:
            return _details(age=age[0])
        elif instance:
            return _details(instance=instance[0])
        else:
            return


def _count(state=None, tag=None):
    try:
        if state:
            instances = ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
            response = "There are {} servers in {} state right now".format(len(list(instances)), state)
        else:
            if tag:
                key,value = tag.split(":")
                instances = ec2.instances.filter(
                    Filters=[{'Name': 'tag:{}'.format(key.title()), 'Values': [value]}])
                response = "There are {} servers with {} tag right now".format(len(list(instances)), tag)
            else:
                instances = ec2.instances.all()
                response = "There are totally {} servers right now".format(len(list(instances)))

        return response
    except ValueError:
        return "The value of tag/state does not match with the input format."


def _details(instance=None, tag=None, age=None):
    instance_running_details = []
    instance_not_running_details = []
    try:
        if tag:
            key,value = tag.split(":")
            instances = ec2.instances.filter(Filters=[{'Name': 'tag:{}'.format(key.title()), 'Values': [value]}])
        elif instance:
            instances = ec2.instances.filter(InstanceIds=List(instance))
        else:
            instances = ec2.instances.all()

        running     = sorted([i for i in instances if i.public_dns_name],
                        key=lambda i : i.launch_time.date(), reverse=True)
         
        not_running = sorted([i for i in instances if not i.public_dns_name], 
                        key=lambda i : i.launch_time.date(), reverse=True)

        if age:
        # refilter by age
            running     = [i for i in running if
                    i.launch_time.date() < date.today() - timedelta(days=int(age))]
            
            not_running = [i for i in not_running if
                    i.launch_time.date() < date.today() - timedelta(days=int(age))]

        response =  "Instance ID--Instance Name--Launch Time\n" + \
                "Running:\n"
        for instance in running:
            response = response + "{} - {} - {}\n".format(
                    instance.id, instance.public_dns_name, instance.launch_time.strftime('%m/%d/%Y'))
        
        response = response + "Not Running:\n"
        for instance in not_running:
            response = response + "{} - {}\n".format(
                    instance.id, instance.launch_time.strftime('%m/%d/%Y'))

        return response
    except ValueError:
        return "The value of tag/state/age does not match with the input format."

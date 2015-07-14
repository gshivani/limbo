# -*- coding: utf-8 -*-
"""!aws <command> returns information on ec2 instances based on given command"""

import boto3
import re
from datetime import date, timedelta

STATES = ['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']

def on_message(msg, server):
    text = msg.get("text", "")
    ec2 = boto3.resource('ec2')
    instance_id = []

    # Extract various features of the text
    tag      = re.findall(r"^!aws.*tag (.*)$", text)
    state    = re.findall(r"^!aws.*state (.*)$", text)
    age      = re.findall(r"^!aws.*age days (.*)$", text)
    instance = re.findall(r"^!aws.*instance (.*)$", text)

    if tag:
        pattern = re.compile('.*:.*')
        if pattern.match(tag) is None:
            return "ERROR: Tag must be in key:value format. Ex: (role:nroute)"

    if state:
        if state not in STATES:
            return "ERROR: State must be one of: {}".format(STATES.join(' ,'))

    if age:
        pattern = re.compile('\d+')
        if pattern.match(age) is None:
            return "ERROR: Age must be a numeric in days. Ex: (age 5)" 

    if instance:
        pattern = re.compile('i-.*')
        if pattern.match(instance) is None:
            return "ERROR: instance format is i-23482221. Ex: (instance i-23482221)"


    # Counting servers
    if re.match(r"^!aws count server$", text):
        if state:
            _count(state=state)
        elif tag:
            _count(tag=tag)
        else:
            _count()

    # Details of servers
    if re.match(r"^!aws details.*$", text):
        if tag:
            _details(tag=tag)
        elif age:
            _details(age=age)
        elif instance:
            _details(instance=instance)
        else:
            return


def _count(state=None, tag=None):
    if state:
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
        response = "There are {} servers in {} state right now".format(len(instances), state)
    else:
        if tag:
            key,value = tag.split(":")
            instances = ec2.instances.filter(
                Filters=[{'Name': 'tag:{}'.format(key), 'Values': [value]}])
            response = "There are {} servers with {} tag right now".format(len(instances), tag)
        else:
            instances = ec2.instances.all()
            response = "There are {} servers with {} tag right now".format(len(instances), tag)

    return response


def _details(state=None, tag=None, age=None):
    instance_running_details = []
    instance_not_running_details = []

    if tag:
        key,value = tag.split(":")
        instances = ec2.instances.filter(Filters=[{'Name': 'tag:{}'.format(key.title), 'Values': [value]}])
    elif instance:
        instances = ec2.instances.filter(InstanceIds=List(instance))
    else:
        instances = ec2.instances.all()

    running     = [instance for i in instances if i.public_dns_name]
    not_running = [instance for i in instances if not i.public_dns_name]

    if age:
        # refilter by age
        running     = [instance for i in running if
                i.launch_time.date() == date.today() - timedelta(days=int(age))]
        not_running = [instance for i in not_running if
                i.launch_time.date() == date.today() - timedelta(days=int(age))]

    response =  "Instance ID--Instance Name--Launch Time\n" + \
                "Running:\n"
    for instance in running:
        response = response + "{} - {} - {}\n".format(
                instance.id, instance.public_dns_name, instance.launch_time.strftime('%m/%d/%Y'))
    for instance in not_running:
        response = response + "{} - {}\n".format(
                instance.id, instance.launch_time.strftime('%m/%d/%Y'))

    return response

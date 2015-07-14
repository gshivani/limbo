# -*- coding: utf-8 -*-
"""!aws <command> returns information on ec2 instances based on given command"""

import boto3
import re
from datetime import date, timedelta

def on_message(msg, server):
    text = msg.get("text", "")
    instance_id = []
    ec2 = boto3.resource('ec2')
    #Counts the ec2 instances
    if re.match(r"^!aws count server$", text):
        instances = ec2.instances.all()
        for instance in instances:
            instance_id.append(instance.id)
        return "There are "+ str(len(instance_id)) + " servers"
    #Counts number of ec2 instances currently running
    elif re.match(r"^!aws count server running$", text):
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            instance_id.append(instance.id)
        return "There are " + str(len(instance_id)) + " servers running right now"
    #Counts the ec2 instances with given tag (Key:Value)
    elif re.match(r"!aws count server with tag (.*)", text):
        try:
            key_value = text.rsplit(None, 1)[-1]
            key,value = key_value.split(":")
            instances = ec2.instances.filter(
                Filters=[{'Name': 'tag:'+key, 'Values': [value]}])
            for instance in instances:
                instance_id.append(instance.id)
            return "There are "+ str(len(instance_id)) + \
            " servers with tag " + key + ":" + value                
        except ValueError:
            return "You have to give me a tag - <key:value>"
    #Displays the details (instance id, instance name and launch time) for the      instance with given tag
    elif re.match(r"^!aws details server with tag (.*)$", text):
       try:
           key_value = text.rsplit(None, 1)[-1]
           key,value = key_value.split(":")
           instance_running_details = []
           instance_not_running_details = []
           instances = ec2.instances.filter(Filters=[{'Name': 'tag:'+key, 'Values': [value]}])
           for instance in instances:
               if (instance.public_dns_name == ''):
                   instance_not_running_details.append(instance.id)
                   instance_not_running_details.append(instance.public_dns_name)
                   lt = instance.launch_time
                   instance_not_running_details.append(lt.strftime('%m/%d/%Y'))
                   instance_not_running_details.append("\n")
               else:
                   instance_running_details.append(instance.id)
                   instance_running_details.append(instance.public_dns_name)
                   lt = instance.launch_time
                   instance_running_details.append(lt.strftime('%m/%d/%Y'))
                   instance_running_details.append("\n")
           return "Instance Id-" + "-Instance Name-" + "-Launch Time" + "\n" + \
           "Running: " + "\n" + " ".join(instance_running_details)+ \
           "Not Running: " + "\n" + " ".join(instance_not_running_details)
       except ValueError:
           return "You have to give me a tag - <key:value>"
    #Displays details of ec2 (instance id, instance name and launch time) of an     instance that has been launched before given number of days.
    elif re.match(r"^!aws details server with age days (.*)$", text):
        try:
            age = text.rsplit(None, 1)[-1]
            instance_running_details = []
            instance_not_running_details = []
            instances = ec2.instances.all()
            if bool(instances):
                return "No server launched " + age + " days ago."
            for instance in instances:
                lt = instance.launch_time
                if (lt.date() == date.today() - timedelta(days=int(age))):
                    if (instance.public_dns_name == ''):
                        instance_not_running_details.append(instance.id)
                        instance_not_running_details.append(instance.public_dns_name)
                        lt = instance.launch_time
                        instance_not_running_details.append(lt.strftime('%m/%d/%Y'))
                        instance_not_running_details.append("\n")
                    else:
                        instance_running_details.append(instance.id)
                        instance_running_details.append(instance.public_dns_name)
                        lt = instance.launch_time
                        instance_running_details.append(lt.strftime('%m/%d/%Y'))
                        instance_running_details.append("\n")
                    return "Instance Id-" + "-Instance Name-" + "-Launch Time" + "\n" + \
                    "Running: " + "\n" + " ".join(instance_running_details) + "Not Running: " + \
                    "\n" + " ".join(instance_not_running_details)  
        except ValueError:
            return "You have to give me a number like '2'"               
    else:
        return 
    
    
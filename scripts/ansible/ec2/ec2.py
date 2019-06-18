#!/usr/bin/python3

import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

def get_public_ips():
    ips = list()
    pips = list()

    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if "Tags" in instance:
                tags = instance["Tags"]
                for tag in tags:
                    if tag["Key"] == "tool" and tag["Value"] == "ansible":
                        if "PublicIpAddress" in instance:
                            ips.append(instance["PublicIpAddress"])
                        if "PrivateIpAddress" in instance:
                            pips.append(instance["PrivateIpAddress"])
    return ips, pips

def list_ips():
    # Variable return is needed to avoid network latency.
    hosts, phosts = get_public_ips()
    inventory = { "group": { "hosts": hosts , "vars": { "ansible_python_interpreter": "/usr/bin/python3", "private_hosts" : phosts }, }, }
    print(inventory)

if __name__ == "__main__":
    list_ips()

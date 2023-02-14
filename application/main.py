# Eliran Turgeman
import logging
# Module boto3 in use to create, configure, and manage AWS services via python
import boto3
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

"""This function will find running instances
with the tags in the filter section."""
def main():
    print('Start')
    #Initialize the boto3 EC2 client
    ec2 = boto3.client('ec2')
    # Define the filters to search for instances
    filters = [
        {'Name': 'tag:k8s.io/role/master', 'Values': ['1']},
        {'Name': 'instance-state-code', 'Values': ['16']}
    ]
    # Search for instances that match the filters
    response = ec2.describe_instances(Filters=filters)
    # Extract the public IP addresses of the instances
    ip_addresses = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ip_addresses.append(instance['PublicIpAddress'])

    if len(ip_addresses) > 0:
        print('This filters:', filters, 'found on those IPs:', ip_addresses)
    else:
        print('No IPs was found with this filters: {}:', filters)

    print('End')


if __name__ == "__main__":
    main()

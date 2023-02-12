# Eliran Turgeman
import boto3
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def main():
    print('start')
    # Initialize the boto3 EC2 client
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
        print("This filters: {} found on those IPs:".format(filters))
        print(ip_addresses)
    else:
        print("No IPs was found with this filters: {}:".format(filters))
    print('end')


if __name__ == "__main__":
    main()

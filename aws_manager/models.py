from django.db import models
import boto3


class AWSNotFoundException(Exception):
    """Server not found at AWS"""

class AWSServer(models.Model):
    """
    AWSServer represents a single EC2 server at AWS
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, null=True, blank=True)
    aws_access_key = models.CharField(max_length=20)
    aws_secret_key = models.CharField(max_length=40)
    aws_region = models.CharField(max_length=20, default='us-east-1')
    user_name = models.CharField(max_length=20, default='Administrator')

    def __unicode__(self):
        return self.name

    def get_connection(self):
        """
        Connects to AWS and returns an ec2 connection
        """
        conn = boto3.client('ec2', region_name=self.aws_region, aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key)
        return conn

    def describe_instance(self):
        """
        Connects to AWS and returns an instance description
        """
        conn = self.get_connection()
        all_instances = conn.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [self.name]}])
        if not all_instances:
            raise AWSNotFoundException("AWS Instance not found, check settings.")
        inst = all_instances['Reservations'][0]['Instances'][0]
        return conn, inst

    def get_instance_id(self):
        """
        Connects to AWS and returns an instance id
        """
        conn, inst = self.describe_instance()
        inst_id = inst['InstanceId']
        return conn, inst_id

    def start_server(self):
        """
        Sends a message to AWS to start the server
        """
        conn, inst_id = self.get_instance_id()
        conn.start_instances(InstanceIds=[inst_id])

    def stop_server(self):
        """
        Sends a message to AWS to stop the server
        """
        conn, inst_id = self.get_instance_id()
        conn.stop_instances(InstanceIds=[inst_id])

    def get_server_state(self):
        """
        returns the state of the server (e.g., 'running', 'stopped')
        """
        _, inst = self.describe_instance()
        return inst['State']['Name']


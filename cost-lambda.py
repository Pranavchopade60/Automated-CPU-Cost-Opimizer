import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

CPU_THRESHOLD = 5

def lambda_handler(event, context):

    print("Lambda Started")

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    print("Instances Found:", len(response['Reservations']))

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:

            instance_id = instance['InstanceId']
            print("Checking:", instance_id)

            end = datetime.utcnow()
            start = end - timedelta(minutes=30)

            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start,
                EndTime=end,
                Period=300,
                Statistics=['Average']
            )

            print(metrics)

    return {
        "statusCode": 200,
        "body": "Done"
    }
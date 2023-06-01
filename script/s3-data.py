import boto3
import json
import csv
from datetime import datetime, timedelta


s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

# Get list of S3 buckets
buckets = s3_client.list_buckets()['Buckets']

# Define CSV filename
csv_file = 's3_buckets.csv'

# Loop through each bucket and write name to CSV file
for bucket in buckets:
    # Get the current date and the date 14 days ago
    today = datetime.now()
    date_14_days_ago = today - timedelta(days=14)

    # Convert the dates to S3 date format
    today_str = today.strftime('%Y-%m-%d')
    date_14_days_ago_str = date_14_days_ago.strftime('%Y-%m-%d')

    # Get a list of all objects in the bucket
    objects = s3.Bucket(bucket['Name']).objects.all()

    # Calculate the size of the objects created or modified on the current date
    today_size = sum([obj.size for obj in objects if obj.last_modified.strftime('%Y-%m-%d') == today_str])

    # Calculate the size of the objects created or modified 14 days ago
    size_14_days_ago = sum([obj.size for obj in objects if obj.last_modified.strftime('%Y-%m-%d') == date_14_days_ago_str])

    try:
        response = s3.get_bucket_location(Bucket=bucket['Name'])
        region = response['LocationConstraint']
    except Exception as e:
        region = 'us-east-1'

    try:
        response = s3.get_bucket_lifecycle_configuration(Bucket=bucket['Name'])
        lifecycle = response['Rules']
    except Exception as e:
        lifecycle = None

    try:
        response = s3.get_bucket_acl(Bucket=bucket['Name'])
        acl = response['Grants']
    except Exception as e:
        acl = None

    try:
        response = s3.get_bucket_logging(Bucket=bucket['Name'])
        logging = response['LoggingEnabled']
    except Exception as e:
        logging = None

    try:
        response = s3.get_bucket_cors(Bucket=bucket['Name'])
        cors = response['CORSRules']
    except Exception as e:
        cors = None

    try:
        response = s3.get_bucket_policy(Bucket=bucket['Name'])
        policy = json.loads(response['Policy'])
    except Exception as e:
        policy = None

    #Differences
    if today_size > size_14_days_ago:
        increased_size = (today_size - size_14_days_ago)
    else:
        increased_size = 0

    bucket_details = {
        'BucketName': bucket['Name'],
        'Region': region,
        today_str: today_size,
        date_14_days_ago_str: size_14_days_ago,
        'Increase': increased_size,
        'Lifecycle': lifecycle,
        'ACL': acl,
        'Logging': logging,
        'CORS': cors,
        'Policy': policy,
    }

    print(json.dumps(bucket_details))
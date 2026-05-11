
import boto3
from boto3.dynamodb.conditions import Attr, Key

# connect to dynamodb resource
dynamodb = boto3.resource('dynamodb')
# connect to the jobs table
table = dynamodb.Table('jobs')
# get a single job by ID
def get_job_from_dynamodb(job_id):
    job = table.get_item(
    Key={
        'job_id': job_id
    })
    if 'Item' in job:
        return job['Item']
    return None

# save job to dynamodb
def save_job_to_dynamodb(jobs):
    no_of_jobs_saved = 0
    job_exists = False
    for job in jobs:
        
        #  check if job already exists in the table
        existing_job = get_job_from_dynamodb(job['job_id'])
        if existing_job is not None:
            job_exists = True
            continue
        table.put_item(Item=job)
        no_of_jobs_saved += 1
    return no_of_jobs_saved

# get all jobs from dynamodb
def get_all_jobs_from_dynamodb(state=None):
    if state:
        response = table.scan(
            FilterExpression=Attr("state").eq(state)
        )
    else:
        response = table.scan()

    return response.get("Items", [])

# update job state in dynamodb
def update_job_state_in_dynamodb(job_id, new_state=None):
    if new_state is not None:
        return table.update_item(
            Key={
                'job_id': job_id
            },
            UpdateExpression=f"SET state = :{new_state}",
            ExpressionAttributeValues={
                ':state': new_state
            }
            returns="ALL_NEW"
        )
        
    return None
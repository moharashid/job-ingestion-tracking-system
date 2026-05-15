import boto3
from boto3.dynamodb.conditions import Attr
import os
# connect to dynamodb resource
dynamodb = boto3.resource('dynamodb')
# connect to the jobs table
JOB_TABLE_NAME = os.getenv(
    "JOB_TABLE_NAME",
    "jobs"
)
PREFERENCES_TABLE_NAME = os.getenv(
    "PREFERENCES_TABLE_NAME",
    "preferences"
)
table = dynamodb.Table(JOB_TABLE_NAME)
pref_table = dynamodb.Table(PREFERENCES_TABLE_NAME)

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
    response = table.update_item(
        Key = {"job_id": job_id},
        UpdateExpression="set #s = :s",
        ExpressionAttributeNames={"#s": "state"},
        ExpressionAttributeValues={":s": new_state},
        ReturnValues="ALL_NEW"
    )

    return response.get("Attributes", None)

# save user preferences to dynamodb
def save_preferences_to_dynamodb(user_id, title, location):
    result =pref_table.put_item(
        Item={
            "user_id": user_id,
            "title": title,
            "location": location
        }
    )
    return result.get("Attributes", None)

# get user preferences from dynamodb
def get_preferences_from_dynamodb(user_id):
    result = pref_table.get_item(
        Key={
            "user_id": user_id
        }
    )
    if "Item" in result:
        return result["Item"]
    return None
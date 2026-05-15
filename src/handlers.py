from src.dynamodb import get_job_from_dynamodb, save_job_to_dynamodb, get_all_jobs_from_dynamodb, update_job_state_in_dynamodb, save_preferences_to_dynamodb, get_preferences_from_dynamodb
from src.processor import process_jobs
from src.fetcher import fetch_jobs
import json
import logging

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


VALID_STATES = ["NEW", "APPLIED", "IGNORED"]

# lambda handler for API Gateway events
def lambda_handler(event, context):
    method = get_event_method(event)
    path = event.get("rawPath", "")

    if method == "POST" and path.endswith("/jobs/fetch_jobs"):
        return event_fetch_jobs(event, context)

    if method == "GET" and path.endswith("/jobs") or "/jobs?" in path:
        return event_get_jobs(event, context)

    if method == "GET" and "/jobs/job" in path:
        return event_get_job(event, context)

    if method == "POST" and path.endswith("/jobs/update"):
        return event_update_job_state(event, context)

    if method == "PUT" and "/jobs/preferences" in path:
        return event_set_preferences(event, context)

    if method == "GET" and "/jobs/preferences" in path:
        return event_get_preferences(event, context)
    
    logger.warning(f"Received unsupported request: {method} {path}")
    return response(404, {"error": "Route not found"})

# helper function to get method from event
def get_event_method(event):
    return event.get("requestContext", {}).get("http", {}).get("method", None)

# helper function for standardized API responses
def response(status, message):
    return {
        "statusCode": status,
        "body": json.dumps(message),
        "headers": {
            "Content-Type": "application/json"
        }
    }
# get one job by id
def event_get_job(event,context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    if get_event_method(event) != "GET":
        return response(405, {"error": "Method Not Allowed"})
        
    parameters= event.get("pathParameters") or {}
    job_id = parameters.get("job_id", None)
    logger.info(f"Received request for job_id:{job_id}")
    if not job_id:
        return response(400, {"error": "Missing job_id in path parameters"})
        
    job = get_job_from_dynamodb(job_id)

    if not job:
        return response(404, {"error": f"Job with ID {job_id} not found"})
    return response(200, job)
    
    
# get jobs by state
def event_get_jobs(event, context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    
    if get_event_method(event) != "GET":
        return response(405, {"error":"Method Not Allowed"})
    
    parameters = event.get("queryStringParameters") or {}
    state = parameters.get("state", None)
    
    if state is None:
        jobs = get_all_jobs_from_dynamodb()
        return response(200, jobs)
        
    state = state.strip().upper()

    if state not in VALID_STATES:
        return response(400, {"error":f"{state} is not a valid state. Valid states are: {', '.join(VALID_STATES)}"})
        
    jobs = get_all_jobs_from_dynamodb(state)
    
    return response(200, jobs)
    

# update job state
def event_update_job_state(event, context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    if get_event_method(event) != "POST":
        return response(405, {"error": "Method Not Allowed"})
        
    body = event.get("body", None)
    
    if body is None or body == "":
        return response(400, {"error": "Missing request body"})
        
    try:
        body_data = json.loads(body)
    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON in request body"})
        
    job_id = body_data.get("job_id", None)
    state = body_data.get("state", None)
    
    # validate input
    if not job_id or not state:
        return response(400, {"error": "Missing job_id or state in request body"})
    
    # ensure state is uppercase and valid
    state = state.strip().upper()
    if state not in VALID_STATES:
        return response(400, {"error": f"Invalid state: {state}"})

    # check if job exists
    existing_job = get_job_from_dynamodb(job_id)
    if not existing_job:
        return response(404, {"error": f"Job with ID {job_id} not found"})

    updated_job = update_job_state_in_dynamodb(job_id, state)
    
    if not updated_job:
        return response(404, {"error": f"Job with ID {job_id} not found"})
        
    return response(200, updated_job)

# fetch jobs from API
def event_fetch_jobs(event, context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    # params = {
    #     'title': 'python',
    #     'location': 'remote',
    # }
    # print(json.dumps(event))
    # logger.info(f"Received event: {json.dumps(event)}")
    preferences = get_preferences_from_dynamodb("default")
    params = {
        'title': preferences.get("title"),
        'location': preferences.get("location")
    }
    if get_event_method(event) != "POST":
        return response(405, {"error": "Method Not Allowed"})
    
    # fetch jobs from API and save to DynamoDB
    jobs = fetch_jobs(params)
    processed_jobs = process_jobs(jobs)
    saved_count = save_job_to_dynamodb(processed_jobs)
    
    return response(200, {"message": f"Fetched {len(processed_jobs)} jobs from API, saved {saved_count} new jobs to DynamoDB"})


# event set preferences
def event_set_preferences(event, context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    if get_event_method(event) != "PUT":
        return response(405, {"error": "Method Not Allowed"})
    
    if event.get("pathParameters") is None:
        return response(400, {"error": "Missing path parameters"})
    
    user_id = event.get("pathParameters", {}).get("user_id")
    if not user_id:
        return response(400, {"error": "Missing user_id in path parameters"})

    body = event.get("body", None)
    if body is None or body == "":
        return response(400, {"error": "Missing request body"})
    try:
        body_data = json.loads(body)
    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON in request body"})
    title = body_data.get("title", None)
    location = body_data.get("location", None)
    if not title or not location:
        return response(400, {"error": "Missing title or location in request body"})
    
    # save preferences to DynamoDB
    preferences = save_preferences_to_dynamodb(user_id, title, location)
    return response(200, {"message": "Preferences saved successfully",
                          "preferences": {
                                "user_id": user_id,
                                "title": title,
                                "location": location
                          }})

# event get preferences
def event_get_preferences(event, context):
    # always log the incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    if get_event_method(event) != "GET":
        return response(405, {"error": "Method Not Allowed"})
    
    parameters= event.get("pathParameters") or {}
    user_id = parameters.get("user_id", None)
    logger.info(f"Received request for user_id:{user_id}")
    preferences = get_preferences_from_dynamodb(user_id)
    if not preferences:
        return response(404, {"error": "Preferences not found"})
    return response(200, preferences)

# curl to test get preferences: curl -X GET https://8g3ti1p029.execute-api.us-east-1.amazonaws.com/prod/jobs/preferences/default
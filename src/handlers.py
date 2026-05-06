from src.api import update_job_state, get_job, get_jobs
import json

VALID_STATES = ["NEW", "APPLIED", "IGNORED"]
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
    if event.get("httpMethod") != "GET":
        return response(405, {"error": "Method Not Allowed"})
        
    parameters= event.get("pathParameters") or {}
    job_id = parameters.get("job_id", None)
    print(f"Received request for job_id:{job_id}")
    if not job_id:
        return response(400, {"error": "Missing job_id in path parameters"})
        
    job = get_job(job_id)

    if not job:
        return response(404, {"error": f"Job with ID {job_id} not found"})
    return response(200, job)
    
    
# get jobs by state
def event_get_jobs(event, context):
    
    if event.get("httpMethod") != "GET":
        return response(405, {"error":"Method Not Allowed"})
    
    parameters = event.get("queryStringParameters") or {}
    state = parameters.get("state", None)
    
    if state is None:
        jobs = get_jobs()
        return response(200, jobs)
        
    state = state.strip().upper()

    if state not in VALID_STATES:
        return response(400, {"error":f"{state} is not a valid state. Valid states are: {', '.join(VALID_STATES)}"})
        
    jobs = get_jobs(state)
    
    return response(200, jobs)
    

# update job state
def event_update_job_state(event, context):
    if event.get("httpMethod") != "POST":
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
    
    if not job_id or not state:
        return response(400, {"error": "Missing job_id or state in request body"})
    
    state = state.strip().upper()
    if state not in VALID_STATES:
        return response(400, {"error": f"Invalid state: {state}"})

    updated_job = update_job_state(job_id, state)
    
    if not updated_job:
        return response(404, {"error": f"Job with ID {job_id} not found"})
        
    return response(200, updated_job)

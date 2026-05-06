from src.handlers import event_get_job, event_get_jobs, event_update_job_state
import json

event_get_all = {
    "httpMethod": "GET",
    "queryStringParameters": None,
    "pathParameters": None,
    "body": None
}
event_get_by_state = {
    "httpMethod": "GET",
    "queryStringParameters": {"state": "APPLIED"},
    "pathParameters": None,
    "body": None
}

event_get_one = {
    "httpMethod": "GET",
    "queryStringParameters": None,
    "pathParameters": {"job_id": "f1aef8a9e83893592b3af8cabf8060948538e9015a74dfd76bf731f0957b7740"},
    "body": None
}

event_update = {
    "httpMethod": "POST",
    "queryStringParameters": None,
    "pathParameters": None,
    "body": json.dumps({
        "job_id": "f1aef8a9e83893592b3af8cabf8060948538e9015a74dfd76bf731f0957b7740",
        "state": "NEW"
    })
}

# print("GET ALL:")
# print(event_get_jobs(event_get_all, None))

# print("\nGET BY STATE:")
# print(event_get_jobs(event_get_by_state, None))

# print("\nGET ONE:")
# print(event_get_job(event_get_one, None))

print("\nUPDATE:")
print(event_update_job_state(event_update, None))
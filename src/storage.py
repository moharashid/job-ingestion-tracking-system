import json
import os
from pathlib import Path
DATA_FILE = '../data/jobs.json'

# load the jobs from the json file, return an empty list if the file doesn't exist or is invalid
# small function to check if file exists
def file_exists(filepath):
    return Path(filepath).exists()

def load_jobs():
    
    if not file_exists(DATA_FILE):
        return []
    
    try:
        
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading jobs from {DATA_FILE}: {e}")
        return []
    
def save_jobs(jobs):
    existing_jobs = load_jobs()
    
    existing_job_ids = {job.get("job_id") for job in existing_jobs if job.get("job_id")}
    # print(f"Existing job IDs: {existing_job_ids}")
    # print(type(existing_job_ids))
    new_jobs = []
    for job in jobs:
        if job['job_id'] not in existing_job_ids:
            new_jobs.append(job)
    all_jobs = existing_jobs + new_jobs
    
    # overwrite file (NOT append)
    with open(DATA_FILE, "w") as f:
        json.dump(all_jobs, f, indent=4)

    return len(new_jobs)
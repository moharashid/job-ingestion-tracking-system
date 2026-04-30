import hashlib

# generate a unique job id based on the job's application URL or a combination of its title, company name, and location
def generate_job_id(job):
    link = job.get('application_url')
    if link:
        base = link
    else:
        base = (
            job.get("title", "") +
            job.get("company", {}).get("name", "") +
            job.get("location", "")
        )
    return hashlib.sha256(base.encode('utf-8')).hexdigest()

# create a normalized job object with the required fields
def normalize_job(job):
    return {
        "job_id": generate_job_id(job),
        "title": job.get("title", ""),
        "company": job.get("company", {}).get("name", ""),
        "location": job.get("location", ""),
        "link": job.get("application_url", ""),
        "created_at": job.get("published"),
        "state": "NEW"
    }
# process the raw job data and return a list of normalized job objects
def process_jobs(raw_jobs):
    return [normalize_job(job) for job in raw_jobs]
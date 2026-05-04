from storage import load_jobs,update_saved_jobs
import logging

# configure logging
# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# constants for valid job states
STATES = ["NEW", "APPLIED", "IGNORED"]
def get_jobs(state = None):
    if state not in STATES and state is not None:
        logger.warning(f"Invalid state filter: {state}. Valid states are: {', '.join(STATES)} For all jobs, leave the state parameter empty .")
        return []
    jobs = load_jobs()
    if state :
        filtered_jobs = [job for job in jobs if job.get("state") == state]
        return filtered_jobs
    return jobs

def get_job(job_id):
    jobs = load_jobs()
    for job in jobs:
        if job.get("job_id") == job_id:
            return job
    logger.warning(f"Job with ID {job_id} not found")
    return None


def update_job_state(job_id, state="NEW"):
    
    state = state.upper()
    if state not in STATES:
        logger.error(f"Invalid state: {state}. Valid states are: {', '.join(STATES)}")
        return None
    else:
        jobs = load_jobs()
        job_found = False
        for job in jobs:
            if job.get("job_id") == job_id:
                old_state = job.get("state", "UNKNOWN")
                job["state"] = state
                job_found = True
                break
        if not job_found:
            logger.warning(f"Job with ID {job_id} not found")
            return None
        
        update_saved_jobs(jobs)
        logger.info(f"Updated job {job_id} from state {old_state} to state: {state}")
        return job



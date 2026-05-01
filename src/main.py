from fetcher import fetch_jobs
from processor import process_jobs
from storage import save_jobs
import logging
import json
# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    params = {
        'title': 'python',
        'location': 'remote',
    }
    # fetch the jobs from the API
    raw_jobs = fetch_jobs(params)
    if not raw_jobs:
        logger.warning("No jobs fetched")
        return []
    # process the raw job data and return a list of normalized job objects
    processed_jobs = process_jobs(raw_jobs)
    logger.info("Processed %d jobs", len(processed_jobs))
    logger.info("Sample processed job: %s", processed_jobs[:3] if processed_jobs else "No jobs to show")
    # save the processed jobs to the json file
    new_jobs = save_jobs(processed_jobs)
    logger.info("Saved %d new jobs", new_jobs)

if __name__ == "__main__":
    main()
    
from fetcher import fetch_jobs
from processor import process_jobs
import logging

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
    raw_jobs = fetch_jobs(params)
    if not raw_jobs:
        logger.warning("No jobs fetched")
        return []
    processed_jobs = process_jobs(raw_jobs)
    logger.info("Processed %d jobs", len(processed_jobs))
    logger.info("Sample processed job: %s", processed_jobs[:3] if processed_jobs else "No jobs to show")
    return processed_jobs

if __name__ == "__main__":
    main()
    
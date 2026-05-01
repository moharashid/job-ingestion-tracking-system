'''
calls API
fetches jobs
'''
import logging
import requests
import time

API_URL = 'https://jobdataapi.com/api/jobs/'

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def fetch_jobs(params, retries=3):
    headers = {
        "User-Agent": "job-tracker/1.0"
    }

    for attempt in range(retries):
        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=5)

            if response.status_code == 429:
                wait_time = 2 ** attempt  # exponential backoff
                logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            data = response.json()
            jobs = data.get("results", [])

            return jobs[:3]

        except requests.exceptions.RequestException as e:
            logger.error(f"fetch_jobs failed: {e}")
            return []

    logger.error("Max retries exceeded")
    return []

    
'''
calls API
fetches jobs
'''
import logging
import requests

API_URL = 'https://jobdataapi.com/api/jobs/'

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def fetch_jobs(params):
    headers = {
        "User-Agent": "job-tracker/1.0"
    }
    
    try:
        response = requests.get(API_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        data = response.json()
        
        # get the job lists
        jobs = data.get("results",[])
        
        if not isinstance(jobs, list):
            logger.error(f"Unexpected API response format")
            return []
        
        logger.info(f"fetched {len(jobs)} jobs")
        
        return jobs[:100]  # Return only the first 100 jobs
    
    except requests.exceptions.RequestException as e:
        logger.error(f"fetch_jobs failed for params={params}: {e}")
        return []

    
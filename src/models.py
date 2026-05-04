import json
sample_job_id = 'abc123'
with open('../test.json' , 'r') as f:
    data = json.load(f)
    # if sample_job_id in data:
    #     print("Job ID exists in the data")
    
    print(data)
    for job in data:
        print(job.get("job_id"))
        if sample_job_id in job:
            print("Job ID exists in the data")
            

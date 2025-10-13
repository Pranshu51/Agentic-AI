from fastapi import FastAPI,Query
from client.rq_client import queue
from queues.worker import process_query

app = FastAPI()

@app.get('/')
def root():
  return{"status": 'server is up and running'}


@app.post('/chat')
def chat(
    query: str = Query(..., description=" The chat query of user")
):
  job = queue.enqueue(process_query, query)

  return {"status": "queued" , "job_id": job.id}
  

@app.get('/job-status')
def get_result(
    job_id: str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}  










# from fastapi import FastAPI, Query
# from client.rq_client import queue
# from queues.worker import process_query
# from rq.job import Job

# app = FastAPI()


# @app.get('/')
# def root():
#     return {"status": 'server is up and running'}


# @app.post('/chat')
# def chat(
#     query: str = Query(..., description=" The chat query of user")
# ):
#     # Enqueue job and keep result for 1 hour
#     job = queue.enqueue(process_query, query, result_ttl=3600)
#     return {"status": "queued", "job_id": job.id}


# @app.get('/job-status')
# def get_result(
#     job_id: str = Query(..., description="Job ID")
# ):
#     # Fetch job using the queue's own connection
#     job = queue.fetch_job(job_id)

#     if not job:
#         return {"error": "Job not found or expired"}

#     return {
#         "job_id": job.id,
#         "status": job.get_status(),  # queued, started, finished, failed
#         "result": job.result  # This now contains the return value from process_query
#     }
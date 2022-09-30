import base64
from datetime import datetime

import pandas as pd
import redis
import rq
import os
import json

import graphsimviz_backend.simqt_evaluator
from graphsimviz_backend.tasks.task_hook import TaskHook
from graphsimviz_backend.mailer import error_notification

qr_r = redis.Redis(host=os.getenv('REDIS_HOST', 'digest_redis'),
                   port=os.getenv('REDIS_PORT', 6379),
                   db=0,
                   decode_responses=False)
rq_tasks = rq.Queue('digest_tasks', connection=qr_r)

r = redis.Redis(host=os.getenv('REDIS_HOST', 'digest_redis'),
                port=os.getenv('REDIS_PORT', 6379),
                db=0,
                decode_responses=True)



def run_task(uid, mode, parameters, set_files):
    def set_status(status):
        r.set(f'{uid}_status', f'{status}')



    # set_progress(0.0, 'Initialized')
    # worker_id = os.getenv('RQ_WORKER_ID')
    # r.set(f'{uid}_worker_id', f'{worker_id}')
    # job_id = os.getenv('RQ_JOB_ID')
    # r.set(f'{uid}_job_id', f'{job_id}')
    # r.set(f'{uid}_started_at', str(datetime.now().timestamp()))
    # task_hook = TaskHook(parameters, set_status, set_result, set_files, set_progress, dispatch_sig_contr_calculation)
    # try:
    #     if mode == 'set':
    #         graphsimviz_backend.digest_executor.run_set(task_hook)
    #     elif mode == 'subnetwork':
    #         graphsimviz_backend.digest_executor.run_subnetwork(task_hook)
    #     elif mode == 'subnetwork-set':
    #         graphsimviz_backend.digest_executor.run_subnetwork_set(task_hook)
    #     elif mode == 'id-set':
    #         graphsimviz_backend.digest_executor.run_id_set(task_hook)
    #     elif mode == 'set-set':
    #         graphsimviz_backend.digest_executor.run_set_set(task_hook)
    #     elif mode == 'cluster':
    #         graphsimviz_backend.digest_executor.run_cluster(task_hook)
    #
    # except Exception as e:
    #     print("Error in DIGEST execution:")
    #     error_notification(f"Error in DIGEST execution for {uid}.\nError indicator: {e}")
    #     r.set(f'{uid}_failed', '1')
    #     import traceback
    #     traceback.print_exc()
    #     set_status(f'{e}')
    #     check_sc_execution(uid)

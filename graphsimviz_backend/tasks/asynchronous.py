import json

from graphsimviz_backend.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name='graphsimviz-job')
def compute_cluster_values(task_id):
    from graphsimviz_backend.models import ClusterTask
    from graphsimviz_backend import simqt_evaluator
    task = ClusterTask.objects.get(UID=task_id)
    request = json.loads(task.request)
    logger.info(f"Started cluster_p_value job {task.UID}")
    result = simqt_evaluator.calculate_cluster_scores(request['network_type1'], request['network_type2'],
                                                      request['id_space'],
                                                      request['nodes'])
    task.done = True
    task.result = json.dumps(result)
    task.save()
    logger.info(f"Finished job {task.UID}")

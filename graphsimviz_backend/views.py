import json
import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response
from graphsimviz_backend import simqt_evaluator
from graphsimviz_backend import networks
from graphsimviz_backend.serializers import ClusterTaskSerializer


@api_view(['POST'])
def get_scores(request) -> Response:
    return Response(simqt_evaluator.calculate(request.data['network_type1'], request.data['network_type2'],
                                              request.data['id_space'], request.data['nodes']))


@api_view(['POST'])
def get_local_scores(request) -> Response:
    print(request.data)
    return Response(simqt_evaluator.calculate_local_scores(request.data['network_type1'], request.data['network_type2'],
                                                           request.data['id_space'], request.data['nodes']))


def create_cluster_task(request):
    from graphsimviz_backend.models import ClusterTask
    try:
        return ClusterTask.objects.get(request=request)
    except ClusterTask.DoesNotExist:
        pass

    uid = str(uuid.uuid4())
    while ClusterTask.objects.filter(UID=uid).exists():
        uid = str(uuid.uuid4())
    task = ClusterTask.objects.create(request=request, UID=uid)
    import graphsimviz_backend.tasks.asynchronous
    graphsimviz_backend.tasks.asynchronous.compute_cluster_values.delay(task.UID)
    return task


@api_view(['POST'])
def get_cluster_scores(request) -> Response:
    print(request.data)
    request.data['nodes'] = list(set(request.data['nodes']))
    task = create_cluster_task(json.dumps(request.data))
    return Response(ClusterTaskSerializer().to_representation(task))


@api_view(['POST'])
def get_global_scores(request) -> Response:
    print(request.data)
    return Response(
        simqt_evaluator.calculate_global_scores(request.data['network_type1'], request.data['network_type2'],
                                                request.data['id_space']))


@api_view(['POST'])
def get_networks(request) -> Response:
    print(request.data)
    return Response(
        networks.get_networks(request.data['network_type1'], request.data['network_type2'], request.data['id_space'],
                              request.data['nodes']))

@api_view(['POST'])
def get_first_neighbor_networks(request) -> Response:
    print(request.data)
    return Response(
        networks.get_first_neighbor_networks(request.data['network_type1'], request.data['network_type2'], request.data['id_space'],
                              request.data['nodes']))

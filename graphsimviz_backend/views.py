import json
import mimetypes
import os
import uuid

from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from graphsimviz_backend import simqt_evaluator
from graphsimviz_backend import networks
from graphsimviz_backend.serializers import ClusterTaskSerializer


@api_view(['POST'])
def get_scores(request) -> Response:
    return Response(
        simqt_evaluator.calculate(request.data['network'], request.data['network_type1'], request.data['network_type2'],
                                  request.data['id_space'], request.data['nodes'], request.data['mwu']))


@api_view(['GET'])
def download_results(request):
    return download_file(os.path.join(simqt_evaluator.get_data_dir(), 'source_data.zip'))

@api_view(['GET'])
def download_data(request):
    return download_file(os.path.join(simqt_evaluator.get_data_dir(), 'results.zip'))



def download_file(file_path):
    if not os.path.exists(file_path):
        return Response({"error": f"File {file_path} not found"}, status=404)
    try:
        # FileResponse will automatically close the file when the response is finished.
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        # Manually setting content type if guessable, though FileResponse does this too.
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type:
            response['Content-Type'] = content_type
        return response
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def get_local_scores(request) -> Response:
    print(request.data)
    return Response(simqt_evaluator.calculate_local_scores(request.data['network'], request.data['network_type1'],
                                                           request.data['network_type2'],
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
        simqt_evaluator.calculate_global_scores(request.data['network'], request.data['network_type1'],
                                                request.data['network_type2'],
                                                request.data['id_space']))


@api_view(['POST'])
def get_networks(request) -> Response:
    print(request.data)
    return Response(
        networks.get_networks(request.data['network'], request.data['network_type1'], request.data['network_type2'],
                              request.data['id_space'],
                              request.data['nodes']))


@api_view(['POST'])
def get_first_neighbor_networks(request) -> Response:
    print(request.data)
    return Response(
        networks.get_first_neighbor_networks(request.data['network_type1'], request.data['network_type2'],
                                             request.data['id_space'],
                                             request.data['nodes']))

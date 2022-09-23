from rest_framework.decorators import api_view
from rest_framework.response import Response
from gvl_backend import simqt_executor


@api_view(['POST'])
def get_scores(request) -> Response:
    return Response(simqt_executor.calculate(request.data['network_type1'], request.data['network_type2'], request.data['id_space'], request.data['nodes']))


@api_view(['POST'])
def get_local_scores(request) -> Response:
    print(request.data)
    return Response(simqt_executor.calculate_local_scores(request.data['network_type1'], request.data['network_type2'], request.data['id_space'], request.data['nodes']))


@api_view(['POST'])
def get_cluster_scores(request) -> Response:
    print(request.data)
    return Response(simqt_executor.calculate_cluster_scores(request.data['network_type1'], request.data['network_type2'], request.data['id_space'], request.data['nodes']))


@api_view(['POST'])
def get_global_scores(request) -> Response:
    print(request.data)
    return Response(simqt_executor.calculate_global_scores(request.data['network_type1'], request.data['network_type2'], request.data['id_space']))

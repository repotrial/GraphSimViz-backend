"""graphsimviz_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from graphsimviz_backend.views import get_scores, get_global_scores, get_cluster_scores, get_local_scores, get_networks, get_first_neighbor_networks
urlpatterns = [
    path('get_scores', get_scores),
    path('get_global_scores', get_global_scores),
    path('get_cluster_scores', get_cluster_scores),
    path('get_local_scores', get_local_scores),
    path('get_networks', get_networks),
    path('get_fist_neighbor_networks', get_first_neighbor_networks),

    # path('update',run_update),
    # path('sig_cont', run_sig_cont)
]

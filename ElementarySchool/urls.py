from django.conf.urls import url
from django.contrib import admin
from .views import plot_choropleth_maps,get_map

app_name= 'district'

urlpatterns = [
    url(r'^$',plot_choropleth_maps,name="plt_maps"),
    url(r'get-data/', get_map, name="get_data"),
]

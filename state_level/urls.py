"""chloropleth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from .views import query_feature,get_districts,get_talukas,base_map
app_name ='choropleth'
urlpatterns = [
    url(r'^$',base_map,name="plt_map"),
    url(r'^get-district/$',get_districts,name="district_name"),
    url(r'^get-taluka/$',get_talukas,name="taluka_name"),
    url(r'^get-query-answer/$',query_feature,name="query_feature"),
]

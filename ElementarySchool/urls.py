from django.conf.urls import url
from django.contrib import admin
from .views import get_dist_count_map, get_features, \
    get_district_security, get_district_sanitation, get_taluka_sanitation,get_highlighted_dist, \
    get_taluka_security, get_taluka_water, get_taluka_count_map, get_water_district

app_name= 'district'

urlpatterns = [
    url(r'^state/(?P<state>[a-zA-Z]{3,})/(?P<feature>[a-zA-Z]{3,})$',get_dist_count_map,name="plt_dist"),
    url(r'^state/(?P<state>[a-zA-Z]{3,})/water-index$',get_water_district,name="wtr_st_ind"),
    url(r'^state/(?P<state>[a-zA-Z]{3,})/sanitation-index$',get_district_sanitation,name="san_st_ind"),
    url(r'^state/(?P<state>[a-zA-Z]{3,})/security-index$',get_district_security,name="sec_st_ind"),
    url(r'^form$',get_features,name="get_feature"),
    url(r'^query_form$',get_highlighted_dist,name="highlight"),
    url(r'^taluka/(?P<district>[a-zA-Z]{3,})/(?P<feature>[a-zA-Z]{3,})$', get_taluka_count_map, name="plt_tlk"),
    url(r'^taluka/water-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_water, name="wtr_tlk_ind"),
    url(r'^taluka/sanitation-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_sanitation, name="san_tlk_ind"),
    url(r'^taluka/security-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_security, name="sec_tlk_ind"),
]


from django.conf.urls import url
from django.contrib import admin
from .views import get_map_count_features_district, get_features, \
    get_district_security, get_district_sanitation, get_taluka_sanitation,get_highlighted_dist, \
    get_taluka_security, get_taluka_water, get_taluka_count_map, get_water_district
app_name= 'district'
urlpatterns = [
    url(r'^teachers$',get_map_count_features_district,{'feature':'teacher'},name="plot_ppteacher"),
    url(r'^students$',get_map_count_features_district,{'feature':'student'},name="plot_ppstudent"),
    url(r'^mag-1$', get_map_count_features_district, {'feature': 'schcat_5'}, name="plot_mg_1"),
    url(r'^mag-2$', get_map_count_features_district, {'feature': 'schmgt_98'}, name="plot_mg_2"),
    url(r'^mag-3$', get_map_count_features_district, {'feature': 'schmgt_3'}, name="plot_mg_3"),
    url(r'^mag-4$', get_map_count_features_district, {'feature': 'schmgt_4'}, name="plot_mg_4"),
    url(r'^water$',get_water_district,name="plot_water"),
    url(r'^sanitation$',get_district_sanitation,name="plot_sanitation"),
    url(r'^security$',get_district_security,name="plot_security"),
    url(r'^form$',get_features,name="get_feature"),
    url(r'^query_form$',get_highlighted_dist,name="highlight"),

    url(r'^taluka/(?P<district>[a-zA-Z]{3,})/(?P<feature>[a-zA-Z]{3,})$', get_taluka_count_map, name="plt_tlk"),
    #url(r'^taluka_student/(?P<district>[a-zA-Z]{3,})$', get_taluka_count_map, {'feature': 'student'}, name="plt__std_tlk"),
    url(r'^taluka/water-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_water, name="wtr_tlk_ind"),
    url(r'^taluka/sanitation-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_sanitation, name="san_tlk_ind"),
    url(r'^taluka/security-index/(?P<district>[a-zA-Z]{3,})$', get_taluka_security, name="sec_tlk_ind"),
    
#url(r'^$',get_base_map,name="base_map"),
]

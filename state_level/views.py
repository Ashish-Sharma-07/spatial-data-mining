# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,Http404
from django.http.response import JsonResponse
from django.core.serializers import serialize
from colour import Color
from django.db.models import Count,Sum
from models import BlockSummary,DistrictSummary,VillageSummary
import json
from django.views.decorators.csrf import csrf_exempt

'''Dynamic Query Dictionaries based on features'''
klass={
    'block_level':BlockSummary,
    'district_level':DistrictSummary,
    'village_level':VillageSummary,
}

water = {
'water_1' :{'<':'water_1__lt', '>' :'water_1__gt', '>=':'water_1__lte', '<=':'water_1__gte',},
'water_2' :{'<':'water_2__lt' , '<=':'water_2__lte', '>' :'water_2__gt'  , '>=':'water_2__gte',},
'water_3' :{'<' : 'water_3__lt', '>' : 'water_3__gt', '>=': 'water_3__lte','<=': 'water_3__gte',},
'water_4' :{'<' : 'water_4__lt','<=': 'water_4__lte','>' : 'water_4__gt','>=': 'water_4__gte',},
'water_5' :{'<' : 'water_5__lt','<=': 'water_5__lte','>' : 'water_5__gt','>=': 'water_5__gte',},
}

sanitation = {
'toiletwater_g' :{'<':'toiletwater_g__lt','<=':'toiletwater_g__lte','>':'toiletwater_g__gt','>=':'toiletwater_g__gte'},
'toiletwater_b' :{'<':'toiletwater_b__lt','<=':'toiletwater_b__lte','>':'toiletwater_b__gt','>=':'toiletwater_b__gte'},
'toiletb_func'  :{'<':'toiletb_func__lt' ,'<=':'toiletb_func__lte' ,'>':'toiletb_func__gt' ,'>=':'toiletb_func__gte'},
'toiletg_func'  :{'<':'toiletg_func__lt' ,'<=':'toiletg_func__lte' ,'>':'toiletg_func__gt' ,'>=':'toiletg_func__gte'},
'urinals_b'     :{'<':'urinals_b__lt' ,'<=':'urinals_b__lte' ,'>':'urinals_b__gt' ,'>=':'urinals_b__gte'},
'urinals_g'     :{'<':'urinals_g__lt' ,'<=':'urinals_g__lte' ,'>':'urinals_g__gt' ,'>=':'urinals_g__gte'},
'handwash_count':{'<':'handwash_count__lt' ,'<=':'handwash_count__lte' ,'>':'handwash_count__gt' ,'>=':'handwash_count__gte'},
}

security = {
'bndrywall_1':{'<':'bndrywall_1__lt','<=':'bndrywall_1__lte','>':'bndrywall_1__gt','>=':'bndrywall_1__gte'},
'bndrywall_2':{'<':'bndrywall_2__lt','<=':'bndrywall_2__lte','>':'bndrywall_2__gt','>=':'bndrywall_2__gte'},
'bndrywall_3':{'<':'bndrywall_3__lt','<=':'bndrywall_3__lte','>':'bndrywall_3__gt','>=':'bndrywall_3__gte'},
'bndrywall_4':{'<':'bndrywall_4__lt','<=':'bndrywall_4__lte','>':'bndrywall_4__gt','>=':'bndrywall_4__gte'},
'bndrywall_5':{'<':'bndrywall_5__lt','<=':'bndrywall_5__lte','>':'bndrywall_5__gt','>=':'bndrywall_5__gte'},
'bndrywall_6':{'<':'bndrywall_6__lt','<=':'bndrywall_6__lte','>':'bndrywall_6__gt','>=':'bndrywall_6__gte'},
'bndrywall_7':{'<':'bndrywall_7__lt','<=':'bndrywall_7__lte','>':'bndrywall_7__gt','>=':'bndrywall_7__gte'},
'bndrywall_8':{'<':'bndrywall_8__lt','<=':'bndrywall_8__lte','>':'bndrywall_8__gt','>=':'bndrywall_8__gte'},
}

school_cat = {
'schcat_1':{'<':'schcat_1__lt','<=':'schcat_1__lte','>':'schcat_1__gt','>=':'schcat_1__gte'},
'schcat_2':{'<':'schcat_2__lt','<=':'schcat_2__lte','>':'schcat_2__gt','>=':'schcat_2__gte'},
'schcat_3':{'<':'schcat_3__lt','<=':'schcat_3__lte','>':'schcat_3__gt','>=':'schcat_3__gte'},
'schcat_4':{'<':'schcat_4__lt','<=':'schcat_4__lte','>':'schcat_4__gt','>=':'schcat_4__gte'},
'schcat_5':{'<':'schcat_5__lt','<=':'schcat_5__lte','>':'schcat_5__gt','>=':'schcat_5__gte'},
'schcat_6':{'<':'schcat_6__lt','<=':'schcat_6__lte','>':'schcat_6__gt','>=':'schcat_6__gte'},
'schcat_7':{'<':'schcat_7__lt','<=':'schcat_7__lte','>':'schcat_7__gt','>=':'schcat_7__gte'},
'schcat_8':{'<':'schcat_8__lt','<=':'schcat_8__lte','>':'schcat_8__gt','>=':'schcat_8__gte'},
'schcat_10':{'<':'schcat_10__lt','<=':'schcat_10__lte','>':'schcat_10__gt','>=':'schcat_10__gte'},
'schcat_11':{'<':'schcat_11__lt','<=':'schcat_11__lte','>':'schcat_11__gt','>=':'schcat_11__gte'},
}

school_management = {
'schmgt_1':{'<':'schmgt_1__lt','<=':'schmgt_1__lte','>':'schmgt_1__gt','>=':'schmgt_1__gte'},
'schmgt_2':{'<':'schmgt_2__lt','<=':'schmgt_2__lte','>':'schmgt_2__gt','>=':'schmgt_2__gte'},
'schmgt_3':{'<':'schmgt_3__lt','<=':'schmgt_3__lte','>':'schmgt_3__gt','>=':'schmgt_3__gte'},
'schmgt_4':{'<':'schmgt_4__lt','<=':'schmgt_4__lte','>':'schmgt_4__gt','>=':'schmgt_4__gte'},
'schmgt_5':{'<':'schmgt_5__lt','<=':'schmgt_5__lte','>':'schmgt_5__gt','>=':'schmgt_5__gte'},
'schmgt_6':{'<':'schmgt_6__lt','<=':'schmgt_6__lte','>':'schmgt_6__gt','>=':'schmgt_6__gte'},
'schmgt_7':{'<':'schmgt_7__lt','<=':'schmgt_7__lte','>':'schmgt_7__gt','>=':'schmgt_7__gte'},
'schmgt_8':{'<':'schmgt_8__lt','<=':'schmgt_8__lte','>':'schmgt_8__gt','>=':'schmgt_8__gte'},
'schmgt_97':{'<':'schmgt_97__lt','<=':'schmgt_97__lte','>':'schmgt_97__gt','>=':'schmgt_97__gte'},
'schmgt_98':{'<':'schmgt_98__lt','<=':'schmgt_98__lte','>':'schmgt_98__gt','>=':'schmgt_98__gte'},
}

teacher = {
'teacher':{'<':'teacher__lt','<=':'teacher__lte','>':'teacher__gt','>=':'teacher__gte',}
}

student = {
'student':{'<':'student__lt','<=':'student__lte','>':'student__gt','>=':'student__gte',}
}

location_fields = {
    'state': 'state__iexact',
    'district':'distname__iexact',
    'taluka':'block_name__iexact',
}

all_features = {}
all_features.update(water)
all_features.update(sanitation)
all_features.update(security)
all_features.update(school_management)
all_features.update(school_cat)
all_features.update(teacher)
all_features.update(student)

@csrf_exempt
def query_feature(request):
    '''Dynamic Feature Based Query Execution'''
    '''Sample Input'''

    sample_input = json.loads(request.POST['data'])
    fld = []
    if sample_input['class'] == 'district_level':
        fld +=['distname']
    elif sample_input['class'] == 'block_level':
        fld += ['distname'];fld +=['block_name']
    else:
        fld += ['distname'];
        fld += ['block_name'];fld +=['village']

    loc = sample_input['location_fields']
    ftr = sample_input['feature_queries']
    loc_query_dict = {location_fields[k]:v for k,v in loc.iteritems()}
    query = klass[sample_input['class']].objects.all()
    for k, v in loc_query_dict.iteritems():
        query = query.filter(**{k:v})


    ## get selected feature dictionary
    query_dict = {}

    for ft in ftr:
        feature = all_features[ft[0]]
        fld +=[ft[0]]
        query_dict.update({feature[ft[1]]: ft[2]})

    #print query_dict

    for k, v in query_dict.iteritems():
        query = query.filter(**{k:v})
    result = query

    if not result:
        raise Http404("No Result to display!!")
    fld = tuple(fld)
    #print(fld)
    result = serialize('geojson',result,geometry_field='geom',fields=fld)

    dist_json = json.loads(result)
    # remove crs field
    dist_json.pop('crs', None)

    result = json.dumps(dist_json)

    return HttpResponse(result)

@csrf_exempt
def get_districts(request):
    if request.method == 'POST':
        if request.is_ajax():
                if request.POST['district']=='True':
                    names = DistrictSummary.objects.only('distname','distcode')
                    names = serialize('json',names,fields=('distname','distcode'))

                    dis_json = json.loads(names)
                    _names = []
                    for dist in dis_json:
                        _names += [dist['fields']]

                    js_dist = json.dumps(_names)

        return HttpResponse(js_dist);
    else:
        raise Http404("Access Denied!");

@csrf_exempt
def get_talukas(request):
    if request.method == 'POST':
        if request.is_ajax():
                if request.POST['district']=='True':
                    names = BlockSummary.objects.filter(distname__iexact=request.POST["district_name"]).only('block_name','blockcode')
                    names = serialize('json',names,fields=('block_name','blockcode'))

                    dis_json = json.loads(names)

                    _names = []
                    for dist in dis_json:
                        _names += [dist['fields']]

                    js_dist = json.dumps(_names)
        return HttpResponse(js_dist);
    else:
        raise Http404("Access Denied!");

def base_map(request):
    water = {
        'water_1':'hand pump',
        'water_2':'well',
        'water_3':'tap water',
        'water_4':'other',
        'water_5':'none',
    }
    sanitation = {
        'toiletwater_g':"Water In Girls Toilet",
        'toiletwater_b':"Water In Boys Toilet",
        'toiletb_func': "Functional Boys Toilet",
        'toiletg_func': "Functional Girls Toilet",
        'urinals_b':"Boys Urinals",
        'urinals_g': "Girls Urinals",
        'handwash_count': "Handwash",
        }

    security = {
        'bndrywall_1':"Pucca",
        'bndrywall_2':"Pucca But Broken",
        'bndrywall_3':"Barbed wire fencing",
        'bndrywall_4':"Hedges",
        'bndrywall_5':"No Boundary wall",
        'bndrywall_6':"Others",
        'bndrywall_7':"Partial",
        'bndrywall_8':"Under Construction",
    }

    school_cat = {
        'schcat_1':'Pri. Only',
        'schcat_2':'Pri. and Upper Pri.',
        'schcat_3':"Pri., Upper Pri., Sec. and Higher Sec.",
        'schcat_4':'Upper Pri.',
        'schcat_5':'Upper Pri., Sec. and Higher Sec.',
        'schcat_6':"Pri., Upper Pri., Sec.",
        'schcat_7':"Upper Pri.,Sec.",
        'schcat_8':'Sec.',
        'schcat_10':'Sec. and Higher Sec.',
        'schcat_11':'Higher Sec.'
    }

    school_management = {
        'schmgt_1':'Edu. Dept.',
        'schmgt_2':'Tribal/social Welfare Dept.',
        'schmgt_3':'Local Body',
        'schmgt_4':'Pvt. Aided',
        'schmgt_5':'Pvt. Unaided',
        'schmgt_6':'Others',
        'schmgt_7':'Central Gov',
        'schmgt_8':'Unrecogised',
        'schmgt_97':'Recog. Madarsa',
        'schmgt_98':'Unrecog. Madarsa'}

    teacher = {'teacher':"No. Of Teachers"}

    student = {'student':"No. Of Students"}

    return render(request,"query.html",context={'wtrAttributes':water,
                                                'sanAttributes':sanitation,
                                                'secAttributes':security,
                                                'schcatAttributes':school_cat,
                                                'schmgtAttributes':school_management,
                                                'tchrAttributes':teacher,
                                                'stdAttributes':student},status=200)

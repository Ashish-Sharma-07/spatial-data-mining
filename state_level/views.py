# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,render_to_response
from django.apps import apps
from django.core.serializers import serialize
from colour import Color
from django.db.models import Count,Sum
from models import SummaryInfo
import json
from .forms import AttributeForm

schoolInfo = apps.get_model('ElementarySchool','SchoolInfo')
districtBoundries = apps.get_model('ElementarySchool','state_maharashtra')
talukaBoundries = apps.get_model('ElementarySchool','taluka_boundaries')

# Create your views here.

def get_info(request):
    d_boundries = districtBoundries.objects.all().order_by('district')

    # serialize the data
    d_geojson = serialize('geojson', d_boundries,geometry_field='geom',fields=('district',))
    dict_json = json.loads(d_geojson)
    # remove crs field
    dict_json.pop('crs', None)
    for i in range(len(d_boundries)):
        d_name = dict_json['features'][i]['properties']['district']
        d_name = d_name.lower()
        d_name = d_name[0].upper()+d_name[1:]
        dict_json['features'][i]['properties'] = get_district_level_data(d_name)
    #dict_json['demo_features'] = d_data
    # convert back to json
    #print dict_json
    d_geojson = json.dumps(dict_json)
    return render(request,'maps.html',{'data':d_geojson,'form':AttributeForm()})

def get_district_level_data(district):
    data = SummaryInfo.objects.values('distname').filter(distname__iexact = district).annotate(
        Sum('school'), Sum('teacher'), Sum('student'),
        Sum('toiletwater_b'), Sum('toiletwater_g'), Sum('toiletb_func'), Sum('urinals_b'), Sum('toiletg_func'),
        Sum('urinals_g'),
        Sum('schcat_1'), Sum('schcat_2'), Sum('schcat_3'), Sum('schcat_4'), Sum('schcat_5'), Sum('schcat_6'),
        Sum('schcat_7'), Sum('schcat_8'), Sum('schcat_10'), Sum('schcat_11'),
        Sum('water_1'), Sum('water_2'), Sum('water_3'), Sum('water_4'), Sum('water_5'),
        Sum('bndrywall_1'), Sum('bndrywall_2'), Sum('bndrywall_3'), Sum('bndrywall_4'), Sum('bndrywall_5'),
        Sum('bndrywall_6'), Sum('bndrywall_7'), Sum('bndrywall_8'),
        Sum('schmgt_1'), Sum('schmgt_2'), Sum('schmgt_3'), Sum('schmgt_4'), Sum('schmgt_5'), Sum('schmgt_6'),
        Sum('schmgt_7'), Sum('schmgt_8'), Sum('schmgt_97'), Sum('schmgt_98'))

    temp = data[0]
    security = {}
    schoolmanagement = {}
    schoolcat = {}
    water = {}
    toilet = {}
    for k,v in temp.iteritems():
        if k.startswith('bndrywall'):
            security[k] = v
        elif k.startswith('schmgt'):
            schoolmanagement[k]=v
        elif k.startswith('schcat'):
            schoolcat[k] = v
        elif k.startswith('toilet') or k.startswith('urinals'):
            toilet[k] = v
        elif k.startswith('water'):
            water[k]=v

    dict_val = {
                    'district':temp['distname'][0].upper()+temp['distname'][1:].lower(),
                    'schools':temp['school__sum'],
                    'student': temp['student__sum'],
                    'teacher': temp['teacher__sum'],
                    'toilet':toilet,
                    'school_management':schoolmanagement,
                    'security':security,
                    'water':water,
                    'school_category':schoolcat,
                    }
    return dict_val


def get_taluka_level_data(district):
    data = SummaryInfo.objects.values('block_name','school','teacher','student','toiletwater_b',
    'toiletwater_g','toiletb_func','urinals_b','toiletg_func','urinals_g','schcat_1','schcat_2',
    'schcat_3','schcat_4','schcat_5','schcat_6','schcat_7','schcat_8','schcat_10','schcat_11',
    'water_1','water_2','water_3','water_4','water_5','bndrywall_1','bndrywall_2','bndrywall_3',
    'bndrywall_4','bndrywall_5','bndrywall_6','bndrywall_7','bndrywall_8','schmgt_1','schmgt_2',
    'schmgt_3','schmgt_4','schmgt_5','schmgt_6','schmgt_7','schmgt_8','schmgt_97','schmgt_98')\
        .filter(distname__iexact=district).order_by('block_name')

    return data
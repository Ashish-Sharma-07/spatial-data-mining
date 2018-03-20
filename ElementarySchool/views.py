# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response, Http404, HttpResponseRedirect, render,HttpResponse
from .models import state_maharashtra, maharashtra_districts,SchoolInfo
from django.core.serializers import serialize
from colour import Color
from django.db.models import Sum, FloatField, Q, F
from django.db.models.functions import Cast
from .forms import AttributeForm
from querybuilder.query import Query
from django.apps.registry import apps
SummaryInfo = apps.get_model('state_level','SummaryInfo')
from django.urls import reverse
import json
from math import floor
from django.http import JsonResponse
from django.template.loader import render_to_string

def get_features(request):
    form = AttributeForm()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.is_ajax():
            print request.POST
            feature = request.POST['feature']
            district = request.POST['district']
            if feature == 'water':
                a = HttpResponseRedirect(reverse('district:wtr_tlk_ind',args=[district]))
            elif feature == 'sanitation':
                a = HttpResponseRedirect(reverse('district:san_tlk_ind',args=[district]))
            elif feature == 'security':
                a = HttpResponseRedirect(reverse('district:sec_tlk_ind',args=[district]))
            else:
                a = HttpResponseRedirect(reverse('district:plt_tlk',args=[district,feature]))
        return HttpResponse(a.url)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AttributeForm()

    return render(request,'chloropleth/form.html',{'form':form})
####################################State#######################################

def get_highlighted_dist(request):
	if request.method == 'POST':
		print(request.is_ajax())
		if request.is_ajax():
			attribute = request.POST['Attribute']
			operator = request.POST['Operator']
			value = request.POST['Value']
			equals_kwargs = {"{}__iexact".format(attribute): value}
			greater_kwargs = {"{}__gt".format(attribute): value}
			less_kwargs = {"{}__lt".format(attribute): value}
			dist_json,length = get_district_boundries()
		
			for i in range(length):
				d_name = dist_json['features'][i]['properties']['district']
				if(operator=='='):
					data = SummaryInfo.objects.values().filter(distname__iexact = d_name,**equals_kwargs)
				elif(operator=='<'):
					data = SummaryInfo.objects.values().filter(distname__iexact = d_name,**less_kwargs)
				elif(operator=='>'):
					data = SummaryInfo.objects.values().filter(distname__iexact = d_name,**greater_kwargs)	
			district = json.dumps(data)
	return render_to_response('chloropleth/maps_query.html',{'district':district})
	
	
def get_district_boundries():
    district = state_maharashtra.objects.all().order_by('district')
    # serialize the data
    district_serialize = serialize('geojson', district,geometry_field='geom',fields=('district',))
    dist_json = json.loads(district_serialize)
    # remove crs field
    dist_json.pop('crs',None)
    for i in range(len(district)):
        d_name = dist_json['features'][i]['properties']['district']
        dist_json['features'][i]['properties']['district'] = d_name[0].upper() + d_name[1:].lower()
    return (dist_json,len(district))

# for schools,teachers,students,schools,school_categories,school_management
def get_map_count_features_district(request,feature):

    dist_json,length = get_district_boundries()
    max_v = 0
    min_v = 1000
    for i in range(length):
        d_name = dist_json['features'][i]['properties']['district']
        features = SummaryInfo.objects.values(feature).filter(distname__iexact = d_name).\
                aggregate(Sum(str(feature)))
        if min_v > features[str(feature)+'__sum']:
            min_v = features[str(feature)+'__sum']
        if max_v < features[str(feature) + '__sum']:
            max_v = features[str(feature) + '__sum']
            rag = max_v - min_v
        dist_json['features'][i]['properties']['feature_val'] = features[str(feature)+'__sum']

    district = json.dumps(dist_json)

    grade = [floor((float(i*rag)/100)+min_v) for i in range(0,110,20)]

    color_list = list(str(i) for i in Color('yellow').range_to(Color('red'), len(grade)))

    return render_to_response('chloropleth/maps.html',{'district':district,'Name':str(feature),'range':rag,
                                                       'grade':grade,'color':color_list})

def get_water_district(request):

    try:
        dark_blue = Color('darkblue')
        light_blue = Color('lightblue')
        color_list = list(str(i) for i in light_blue.range_to(dark_blue,5))

        dist_json,length = get_district_boundries()
        max_v = 0
        min_v = 1000
        weights = ['',0.2,0.2,0.2,0.2,0.2]

        for i in range(length):

            d_name = dist_json['features'][i]['properties']['district']
            water_info = list(SummaryInfo.objects.values('distname').filter(distname__iexact=d_name). \
                              annotate(water_index=
                                       Cast(Sum('water_1'), FloatField()) * weights[1] +
                                       Cast(Sum('water_2'), FloatField()) * weights[2] +
                                       Cast(Sum('water_3'), FloatField()) * weights[3] +
                                       Cast(Sum('water_4'), FloatField()) * weights[4] +
                                       Cast(Sum('water_5'), FloatField()) * weights[5]))[0]
            temp = water_info['water_index']
            max_v = max(temp,max_v)
            min_v = min(temp,min_v)

            dist_json['features'][i]['properties']['feature_val'] = temp
        district = json.dumps(dist_json)
        range_value = max_v - min_v
        feature = "Drinking Water"
        grade = [round(min_v+(float(i * range_value) / 100), 2) for i in range(0, 110, 20)]

        return render_to_response('chloropleth/maps.html',{'district':district,'Name':str(feature),'range':range_value,
                                                       'grade':grade,'color':color_list})
    except IndexError ,e:
        raise Http404("Nope")

def get_district_sanitation(request):

    try:
        sanitation_cols = ['toiletb_func', 'urinals_b', 'toiletg_func', 'urinals_g']
        wt = ['',0.2,0.3,0.2,0.1,0.3]
        # these 2 attributes are yet to be considered
        extra = ['toiletwater_b', 'toiletwater_g']
        max_v = 0
        min_v = 1000
        dist_json,length = get_district_boundries()

        for i in range(length):

            d_name = dist_json['features'][i]['properties']['district']
            # vals_dict contains all 4 attributes and handwash_yn and their total for the particular district

            temp = list(SummaryInfo.objects.values('distname').filter(distname__iexact=d_name).annotate(
                sanitation_index =
                Cast(Sum('toiletb_func'), FloatField()) * wt[1] +
                Cast(Sum('urinals_b'), FloatField()) * wt[2] +
                Cast(Sum('toiletg_func'), FloatField()) * wt[3] +
                Cast(Sum('urinals_g'), FloatField()) * wt[4] +
                Cast(Sum('handwash_count'), FloatField()) * wt[5]
            ))[0]

            max_v = max(max_v,temp['sanitation_index'])
            min_v = min(min_v, temp['sanitation_index'])
            dist_json['features'][i]['properties']['feature_val'] = temp['sanitation_index']

        range_value = max_v - min_v
        district = json.dumps(dist_json)
        grade = [round((float(i * range_value) / 100)+min_v, 2) for i in range(0, 110, 20)]
        dark_blue = Color('#F0DC82')
        light_blue = Color('#8A3324')
        color_list = list(str(i) for i in light_blue.range_to(dark_blue, 5))
        feature = "Sanitation"
        return render_to_response('chloropleth/maps.html',{'district':district,'Name':str(feature),'range':range_value,
                                                       'grade':grade,'color':color_list})
    except IndexError:
        raise Http404('Nope')


def get_district_security(request):

    try:
        # for reference
        labels = ['Not Applicable', 'Pucca', 'Pucca but broken', 'barbed wire fencing', 'Hedges',
                  'No boundary wall', 'others', 'Partial', 'Under Construction']
        # weights corresponds to the labels above
        wt = ['',0.1, 0.6, 0.4, 0.8, 0.7, 0, 0.3, 0.5, 0.2]
        # dist_weight contain key as district and value as its overall weighted average of bndry walls

        max_v = 0
        min_v = 1000
        dist_json, length = get_district_boundries()

        for i in range(length):
            d_name = dist_json['features'][i]['properties']['district']
            temp = list(SummaryInfo.objects.values('distname').filter(distname__iexact=d_name).annotate(
                security_index =
                Cast(Sum('bndrywall_1'), FloatField()) * wt[1] +
                Cast(Sum('bndrywall_2'), FloatField()) * wt[2] +
                Cast(Sum('bndrywall_3'), FloatField()) * wt[3] +
                Cast(Sum('bndrywall_4'), FloatField()) * wt[4] +
                Cast(Sum('bndrywall_5'), FloatField()) * wt[5] +
                Cast(Sum('bndrywall_6'), FloatField()) * wt[6] +
                Cast(Sum('bndrywall_7'), FloatField()) * wt[7] +
                Cast(Sum('bndrywall_8'), FloatField()) * wt[8]
            ))[0]

            max_v = max(max_v, temp['security_index'])
            min_v = min(min_v, temp['security_index'])

            dist_json['features'][i]['properties']['feature_val'] = temp['security_index']
        range_value = max_v - min_v

        district = json.dumps(dist_json)
        grade = [round((float(i * range_value) / 100)+min_v, 2) for i in range(0, 110, 20)]
        dark_blue = Color('#66023C')
        light_blue = Color('#C71585')
        color_list = list(str(i) for i in light_blue.range_to(dark_blue, 5))
        feature = "Security"

        return render_to_response('chloropleth/maps.html',
                                  {'district': district, 'Name': str(feature), 'range': range_value,
                                   'grade': grade, 'color': color_list})
    except IndexError ,e:
        print str(e)
        raise Http404('Nope')

####################################District####################################

def get_taluka_boundries(district):

    taluka = maharashtra_districts.objects.filter(district__iexact=district)
    # serialize the data
    taluka_serialize = serialize('geojson', taluka,geometry_field='geom',fields=('district','taluka'))
    taluka_json = json.loads(taluka_serialize)
    # remove crs field
    taluka_json.pop('crs',None)
    for i in range(len(taluka)):
        d_name = taluka_json['features'][i]['properties']['district']
        taluka_json['features'][i]['properties']['district'] = d_name[0].upper() + d_name[1:].lower()
        t_name = taluka_json['features'][i]['properties']['taluka']
        taluka_json['features'][i]['properties']['taluka'] = t_name[0].upper() + t_name[1:].lower()
    return (taluka_json,len(taluka))

def get_taluka_count_map(request,district,feature):

    max_v = 0
    min_v = 1000
    taluka_json,length = get_taluka_boundries(district)

    for i in range(length):
        t_name = taluka_json['features'][i]['properties']['taluka']
        features = list(SummaryInfo.objects.values(str(feature),'block_name').\
                        filter(Q(block_name__iexact=t_name),Q(distname__iexact = district)))
        if features:
            temp = features[0][str(feature)]
            max_v = max(temp, max_v)
            min_v = min(temp, min_v)
            taluka_json['features'][i]['properties']['feature_val'] = features[0][str(feature)]
        else:
        #    print t_name
            taluka_json['features'][i]['properties']['feature_val'] = ""

    taluka = json.dumps(taluka_json)
    range_val = max_v-min_v
    grade = [round((float(i * range_val) / 100)+min_v,0) for i in range(0, 110, 20)]

    color_list = list(str(i) for i in Color('yellow').range_to(Color('red'), len(grade)))
    return render_to_response('chloropleth/maps.html', {'district': taluka, 'Name': str(feature), 'range': range_val,
                                                               'grade': grade, 'color': color_list})

def get_taluka_water(request,district):
    try:
        dark_blue = Color('darkblue')
        light_blue = Color('lightblue')
        color_list = list(str(i) for i in light_blue.range_to(dark_blue, 5))
        # fields=('district',))
        # create a dictionary
        taluka_json,length = get_taluka_boundries(district)
        max_v = 0
        min_v = 1000
        weights = ['', 0.6, 0.2, 0, 1, 0]
        for i in range(length):
            t_name = taluka_json['features'][i]['properties']['taluka']
            water_info = list(SummaryInfo.objects.values('block_name').filter(block_name__iexact=t_name). \
                              annotate(water_index=
                                       F('water_1') * weights[1] +
                                       F('water_2') * weights[2] +
                                       F('water_3') * weights[3] +
                                       F('water_4') * weights[4] +
                                       F('water_5') * weights[5]))
            if water_info:
                temp = water_info[0]['water_index']
                max_v = max(temp, max_v)
                min_v = min(temp, min_v)
                taluka_json['features'][i]['properties']['feature_val'] = temp

            else:
        #        print t_name
                taluka_json['features'][i]['properties']['feature_val'] = ""

        range_value = max_v -min_v
        feature = "Drinking Water"
        grade = [round((float(i * range_value) / 100)+min_v, 2) for i in range(0, 110, 20)]
        taluka = json.dumps(taluka_json)
        range_value = max_v - min_v
        return render_to_response('chloropleth/maps.html',
                                  {'district': taluka, 'Name': str(feature), 'range': range_value,
                                   'grade': grade, 'color': color_list})
    except IndexError, e:
        raise Http404("Nope")

def get_taluka_sanitation(request,district):

    try:
        dark_color = Color('#F0DC82')
        light_color= Color('#8A3324')
        color_list = list(str(i) for i in dark_color.range_to(light_color, 5))
        max_v = 0
        min_v = 1000
        sanitation_cols = ['toiletb_func', 'urinals_b', 'toiletg_func', 'urinals_g']
        # these 2 attributes are yet to be considered
        extra = ['toiletwater_b', 'toiletwater_g']
        weights = [0.14]*7
        # dist_weight contain key as district and value as its overall count of toilets
        tal_weight = dict()

        taluka_json,length = get_taluka_boundries(district)

        for i in range(length):
            t_name = taluka_json['features'][i]['properties']['taluka']
            san_info = list(SummaryInfo.objects.values('block_name','toiletwater_b','urinals_b',
            'toiletb_func','toiletwater_g','toiletg_func','urinals_b','handwash_count').
                            filter(block_name__iexact=t_name))
            if san_info:
                temp_dict = san_info[0]
                t1 = temp_dict['toiletwater_g']
                t2 = temp_dict['toiletwater_b']
                t3 = temp_dict['toiletb_func']
                t4 = temp_dict['toiletg_func']
                t5 = temp_dict['toiletwater_g']
                t6 = temp_dict['toiletwater_g']
                t7 = temp_dict['handwash_count']
                temp = t1*weights[0]+t2*weights[1]+t3*weights[2]+t4*weights[3]+t5*weights[4]+t6*weights[5]+t7*weights[6]
                temp = round(temp,2)
                max_v = max(temp, max_v)
                min_v = min(temp, min_v)
                taluka_json['features'][i]['properties']['feature_val'] = temp
            else:
                #print t_name
                taluka_json['features'][i]['properties']['feature_val'] = ""

        range_value = max_v -min_v
        taluka = json.dumps(taluka_json)
        grade = [round(min_v+(float(i * range_value)) / 100, 2) for i in range(0, 110, 20)]
        feature = "Sanitation"
        return render_to_response('chloropleth/maps.html',
                                  {'district': taluka, 'Name': str(feature), 'range': range_value,
                                   'grade': grade, 'color': color_list})
    except IndexError, e:
        print str(e)
        raise Http404('Nope')

def get_taluka_security(request,district):

    try:
        # for reference
        labels = ['Not Applicable', 'Pucca', 'Pucca but broken', 'barbed wire fencing', 'Hedges',
                  'No boundary wall', 'others', 'Partial', 'Under Construction']
        max_v = 0
        min_v = 1000

        # weights corresponds to the labels above
        weights = ['', 0.1, 0.6, 0.4, 0.8, 0.7, 0, 0.3, 0.5, 0.2]

        # dist_weight contain key as district and value as its overall weighted average of bndry walls
        taluka_json,length = get_taluka_boundries(district)

        for i in range(length):
            t_name = taluka_json['features'][i]['properties']['taluka']
            security_info = list(SummaryInfo.objects.values('block_name').filter(block_name__iexact=t_name). \
                              annotate(security_index=
                                       F('bndrywall_1') * weights[1] +
                                       F('bndrywall_2') * weights[2] +
                                       F('bndrywall_3') * weights[3] +
                                       F('bndrywall_4') * weights[4] +
                                       F('bndrywall_5') * weights[5] +
                                       F('bndrywall_6') * weights[6] +
                                       F('bndrywall_7') * weights[7] +
                                       F('bndrywall_8') * weights[8])

                              )
            if security_info:
                temp = security_info[0]['security_index']
                max_v = max(temp, max_v)
                min_v = min(temp, min_v)
                taluka_json['features'][i]['properties']['feature_val'] = temp

            else:
#                print t_name
                taluka_json['features'][i]['properties']['feature_val'] = ""

        range_value = max_v-min_v
#        print max_v,min_v
#        print range_value
        taluka = json.dumps(taluka_json)
        grade = [round((float(i * range_value) / 100)+min_v, 2) for i in range(0, 110, 20)]

        dark_color = Color('#66023C')
        light_color = Color('#C71585')
        color_list = list(str(i) for i in light_color.range_to(dark_color, 5))
        feature = "Security"
        return render_to_response('chloropleth/maps.html',
                                  {'district': taluka, 'Name': str(feature), 'range': range_value,
                                   'grade': grade, 'color': color_list})
    except IndexError, e:
        print str(e)
        raise Http404('Nope')

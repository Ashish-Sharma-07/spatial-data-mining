from django import forms
from .models import state_maharashtra,maharashtra_districts

class AttributeForm(forms.Form):
    level = (
        ('district','District'),
        ('taluka','Taluka'),
    )

    district = tuple([(i['district'],i['district'][0].upper()+i['district'][1:].lower()) for i in maharashtra_districts.objects.values('district','id_2').distinct().order_by('id_2')])
    feature = (
        ('teacher','Teacher'),
        ('water','Water'),
        ('student','Student'),
        ('sanitation', 'Sanitation'),
        ('security', 'Security'),
    )

    get_level = forms.ChoiceField(label='Level',choices=level,initial='district')
    get_district = forms.ChoiceField(label='District',choices=district,disabled=True)
    get_feature = forms.ChoiceField(label='Feature',choices = feature)

class QueryForm(forms.Form):
	Operators = (('equalsto','EQUALS TO'),('less_than','LESS THAN'),('greater_than','GREATER THAN'))
	My_attribute = forms.ChoiceField(label='attribute',choices=[],initial='select attribute',widget=forms.Select(attrs={'class': 'select', 'id': 'attr_select'}))
	My_operator = forms.ChoiceField(label='Operator',choices=Operators,initial='operator')
	Value= forms.CharField(label='value')

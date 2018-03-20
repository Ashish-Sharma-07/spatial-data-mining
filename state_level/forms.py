from django import forms
from .models import SummaryInfo

class AttributeForm(forms.Form):
    level = (
        ('district','District'),
        ('taluka','Taluka'),
    )

    district = tuple([(i['distname'],i['distname']) for i in SummaryInfo.objects.values('distname').distinct().order_by('distname')])
    feature = (
        ('ppteacher','Teacher'),
        ('water','Water'),
        ('ppstudent','Student'),
        ('sanitation', 'Sanitation'),
        ('security', 'Security'),
    )

    get_level = forms.ChoiceField(label='Level',choices=level,initial='district')
    get_district = forms.ChoiceField(label='District',choices=district,disabled=True)
    get_feature = forms.ChoiceField(label='Feature',choices = feature)
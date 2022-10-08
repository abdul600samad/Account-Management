from pyexpat import model
from random import choices
from inventory.models import atten
from django import forms 
class attenform(forms.ModelForm):
    class Meta:
        model=atten
        fields="__all__"
        day_choice=(
            ('monday','Monday'),
            ('tuesday','Tuesday'),
            ('wednesday','Wednesday'),
            ('thursday','Thursday'),
            ('friday','Friday'),
            ('saturday','Saturday'),
            ('sunday','Sunday'),
        )
        labels={'id':'ID','day':'Days','mudeem':'Mudeem','mudeem_hour':'Mudeem Hours',  'najim':'Najim','najim_hour':'Najim Hours','nijam':'Nijam','nijam_hour':'Nijam Hours'}

        widgets={
            'id':forms.NumberInput(attrs={'class':'form-control mb-3'}),
            'day':forms.Select(choices=day_choice,attrs={'class':'form-control mb-3'}),
            'mudeem':forms.NumberInput(attrs={'class':'form-control mb-3'}),
            'najim':forms.NumberInput(attrs={'class':'form-control mb-3'}),
            'nijam':forms.NumberInput(attrs={'class':'form-control'}),
            'mudeem_hour':forms.NumberInput(attrs={'class':'form-control'}),
            'najim_hour':forms.NumberInput(attrs={'class':'form-control'}),
            'nijam_hour':forms.NumberInput(attrs={'class':'form-control'}),

        }

    
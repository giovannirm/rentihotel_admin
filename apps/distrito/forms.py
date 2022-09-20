from django import forms
from .models import Distrito
from provincia.models import Provincia
from settings import * 

class DistritoForm(forms.ModelForm):
    #provincia = forms.ModelChoiceField( queryset= Provincia.objects.all(), label='departamento', widget=forms.Select  )

    class Meta:
        model = Distrito
        fields = '__all__'
    
    class Media:
        js = ('distrito.js')

    def __init__(self, *args, **kwargs):
        super(DistritoForm, self).__init__(*args, **kwargs)
        self.fields['provincia'].queryset = Provincia.objects.none()
        
    
    


#w = DistritoForm()
#print(w.media)
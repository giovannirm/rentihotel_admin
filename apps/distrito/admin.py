from django.contrib import admin
from .models import Distrito
from .forms import DistritoForm



class Distrito_Admin(admin.ModelAdmin):
    #form = DistritoForm
    list_display =('codigo', 'nombre')

    '''
    from provincia.models import Provincia

    def formfield_for_foreignkey(self, db_field, request, **kwargs):    
        print(db_field.name) 
        if db_field.name == "provincia":
            kwargs["queryset"] = Provincia.objects.filter(departamento=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    '''



admin.site.register(Distrito, Distrito_Admin)
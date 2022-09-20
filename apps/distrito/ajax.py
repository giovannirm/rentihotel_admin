from django.http import JsonResponse
from provincia.models import Provincia

def get_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if departamento_id:
        provincias = Provincia.objects.filter(estado_id=estado_id)   
    for provincia in provincias:
        options += '<option value="%s">%s</option>' % (
            provincia.pk,
            provincia.nombre
        )
    response = {}
    response['provincias'] = options
    return JsonResponse(response)

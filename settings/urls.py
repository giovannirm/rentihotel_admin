# coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from usuario import views

from rest_framework.documentation import include_docs_urls

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API - RENTI')


urlpatterns = [
	url(r'^grappelli/', include('grappelli.urls')),
    url('admin/', admin.site.urls),
    url(r'^', include('website.urls')),
  
    url('', include('social_django.urls', namespace='social')),
    #url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^v1/api/',include('usuario.urls', namespace='users')),

    url(r'^v1/api/',include('cliente.urls', namespace='cliente')),
	url(r'^v1/api/',include('hospedante.urls', namespace='hospedante')),    

	url(r'^v1/api/',include('registrocliente.urls')),   
    url(r'^v1/api/',include('reserva.urls')),    
    #url(r'^v1/api/',include('reservaDetalle.urls')),
    url(r'^v1/culqi/',include('pagoculqi.urls',namespace='pagosCulqi')),

    url(r'^v1/api/',include('registro.urls')), 
    #url(r'^v1/api/',include('registrohabitacion.urls')), 
    url(r'^v1/api/',include('registroadicional.urls')), 


    url(r'^v1/api/',include('hotel.urls')),
	url(r'^v1/api/',include('habitacion.urls')),
    url(r'^v1/api/',include('tipohabitacion.urls')),

    url(r'^v1/api/',include('tiempo.urls')),
    url(r'^v1/api/',include('adicional.urls')), 
	url(r'^v1/api/',include('parametro.urls')),    	

    url(r'^v1/api/',include('pais.urls')),
    url(r'^v1/api/',include('departamento.urls')),  
      
    #url(r'^v1/api/',include('provincia.urls')),
    #url(r'^v1/api/',include('distrito.urls')),
        
    url(r'^get-token/$', views.csrf),
    url('swagger-docs',schema_view),
    url(r'^docs/', include_docs_urls(title='API-RENTI'))
    #url(r'^chaining/', include('smart_selects.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


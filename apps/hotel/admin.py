from django.contrib import admin
from .models import Hotel

from django.utils.html import format_html
from settings import MEDIA_URL

class Hotel_Admin(admin.ModelAdmin):
    list_display =('id','nombre', 'direccion','image_tag')
    ordering = ('id',)

    def image_tag(self, obj):
        return format_html('<img src="{}{}" width="50" height="50"/>'.format(MEDIA_URL,obj.logo))       
    
    image_tag.short_description = 'logo'
   
    

admin.site.register(Hotel, Hotel_Admin)
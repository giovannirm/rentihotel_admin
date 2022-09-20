from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # cifrado la contrseña
from .models import User

class CustomUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ('id','email', 'username','tipo_usuario','is_staff','is_active')
    #search_fields = ('email', 'username',)

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date','pais','tipo_usuario')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
       (None, {'fields': ('email','is_staff','is_active','tipo_usuario','birth_date','pais')}),
    )

admin.site.register(User, CustomUserAdmin)
from rest_framework import permissions
#print(request.user)    # usuario actual
#print(obj.id)          # recurso 


class IsOwner(permissions.BasePermission):
    message = "You must be the owner of this object."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):   ## probrar en postman      
        return bool(obj.id == request.user.id)
class IsAdmin(permissions.BasePermission):
    message = "You must be the admin of this object."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff)
class IsOwnerOrAdmin(permissions.BasePermission):
    message = 'You must be the owner or admin of this object.'
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return bool(obj.id == request.user.id or request.user.is_staff)


class IsAuthenticatedAndAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
class IsAuthenticatedAndOwner(permissions.BasePermission):
    message = 'You must be the owner of this object.'
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

#-----------------------

class IsUserManagment(permissions.BasePermission):
    message = "You cannot log in with the credentials provided."
    def has_permission(self, request, view):
        #print(request.user.tipo_usuario)  
        if request.user and request.user.is_authenticated and  request.user.tipo_usuario != 'CLIENTE':
            return True
        return False 
    #Falta evaluar en funcion a los permisos de usuario --> DjangoModelPermissions
    def has_object_permission(self, request, view, obj):
        #print(obj)
        return True



from rest_framework.permissions import (DjangoModelPermissions)
class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        print(self)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


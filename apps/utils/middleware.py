import redis
from django.utils.deprecation import MiddlewareMixin
#from django.shortcuts import get_current_site
#from rest_framework_jwt.utils import jwt_decode_handler
from django.http import HttpResponse
import json

redis_connection = redis.Redis(host='localhost', port=6379, db=1)

class ValidateTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):    
        try:
            authorization = request.headers['Authorization']
        except KeyError:
            return None
        token = authorization.split()[1]
        validateToken = redis_connection.get(token)
        if validateToken is None:
            #Significa que el token no esta en listblack entonces es valido si aun no ha expirado
            return None
        response_data = {}  
        print(validateToken)          
        response_data['message'] = 'Signature has expired.'
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=403)



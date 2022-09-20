import re
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as auth_logout
from django.middleware.csrf import get_token

from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from utils.send_mail import account_activation_token
from utils.permission import  IsAdmin,IsOwner,IsOwnerOrAdmin
from .models import User
from .serializers import UserSerializers , ChangePasswordSerializer ,ResetPasswordSerializer ,UserDetailSerializers

from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler , jwt_decode_handler
from settings import SECRET_KEY , redis_connection

from social_core.actions import do_complete
from social_django.views import complete,_do_login
from social_core import strategy
from social_django.utils import psa

## MOD - RESERVA
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

class UserRegistrationView(APIView):
    model = User
    permission_classes = ()
    def post(self,request,format=None):  
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=False)                
        user = User.objects.get(email=serializer.data['email'])
        
        try :
            mail_subject = 'Verificación de correo'
            message = render_to_string('verify_account.html', {
                    'user': user,
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
            })
            mail = EmailMessage( mail_subject, message, to=[user.email])
            mail.content_subtype = 'html'
            mail.send() 
        except Exception as e :
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        return Response({'message':'Confirm your email address to complete the registration.'}, status=status.HTTP_200_OK)

class ConfirmRegistrationView(APIView):
    permission_classes = ()
    def get(self, request, uidb64, token):
        try :
            user_id = force_text(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk=user_id)
        except( UnicodeDecodeError,TypeError, ValueError, OverflowError, User.DoesNotExist):          
            return Response({ 'message': 'The activation link is not valid.'},status=status.HTTP_400_BAD_REQUEST)   
        #print(user.is_active)
        if user.is_active is False :
            if user and account_activation_token.check_token(user, token) :
                user.is_active = True
                user.save()
                return Response({ 'message': ' You have successfully verified your email.'},status=status.HTTP_200_OK)
            else: 
                return Response({ 'message': 'The activation link is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'message': 'You have successfully verified your email.'},status=status.HTTP_200_OK)
        

class ResetPasswordView(APIView):
    permission_classes = ()
    def post(self,request,format=None):
        email = request.data.get('email')
        if email :
            try:
                user = User.objects.get(email = email)
            except User.DoesNotExist:
                return Response({'message': 'No user is associated with this email address' }, status=status.HTTP_404_NOT_FOUND)

            mail_subject = 'Restablecer contraseña'                                    
            message = render_to_string('password_reset.html', {                
                'user': user,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            mail = EmailMessage( mail_subject, message, to=[user.email])
            mail.content_subtype = 'html'
            mail.send() 

            return Response({ 'message': 'An email has been sent to account'},status=status.HTTP_200_OK)
        
        return Response({ 'message': 'Request could not be performed with received data.'}, status=status.HTTP_400_BAD_REQUEST)

# comprobar url
class PasswordResetConfirmView(APIView):
    permission_classes = ()        
    def get(self, request, uidb64, token):
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk=user_id)
            #print(user)
        except(UnicodeDecodeError,TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({ 'message': 'The activation link is not valid.'},status=status.HTTP_400_BAD_REQUEST)           
        if user and account_activation_token.check_token(user, token):   
             return Response({ 'message': 'The activation link is valid'},status=status.HTTP_200_OK)
        return Response({ 'message': 'The activation link is not valid.'},status=status.HTTP_400_BAD_REQUEST)

class PasswordResetComplete(APIView):
    permission_classes = ()  
    def post(self, request, uidb64=None, token=None, *arg, **kwargs):      
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,UnicodeDecodeError, User.DoesNotExist):
            user = None
        if user and account_activation_token.check_token(user, token):
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password= serializer.validated_data['new_password2']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'},status=status.HTTP_200_OK)
        return Response({'message': 'The link is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

class AccountLogoutView(APIView):
    permission_classes = ([IsOwner , IsAuthenticated])
    def post(self,request):
        authorization = request.headers['Authorization']
        token = authorization.split()[1]       
        redis_connection.set(token,token)
        redis_connection.expire(token, 21600)
        #print(redis_connection.ttl(token))
        return Response({ 'message':'Logout success' }, status=status.HTTP_200_OK)

# incluir cerrar sesion si cambia password falta arreglar 
class ChangePasswordView(APIView):
    model = User
    permission_classes = ([IsAuthenticated,])
   
    def get_object(self,queryset=None):
        return self.request.user
    
    def put(self,request,*args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():            
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirmed_password = serializer.data.get('confirmed_password')
            #print(check_password(old_password, user.password))
            if check_password(old_password, user.password):  
                if new_password == confirmed_password:                    
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password updated successfully'},status=status.HTTP_200_OK)    

                return Response({'message': 'Password must be confirmed correctly.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## AUTHENTICATION SOCIAL
@psa()
def auth_by_token(request, backend):
    """Decorator that creates/authenticates a user with an access_token"""
    token = request.data.get('access_token')
    user = request.user
    user = request.backend.do_auth(access_token=request.data.get('access_token'))
   
    if user:
        return user
    else:
        return None

class JwtSocialAuthView(APIView):
    permission_classes = ()
    def post(self, request, format=None):
        auth_token = request.data.get('access_token', None)
        backend = request.data.get('backend', None)
        if auth_token and backend:
            try:
                # Try to authenticate the user using python-social-auth
                user = auth_by_token(request, backend)
                # print(user)
            except Exception as e:
                return Response({
                        'status': 'Bad request',
                        'message': str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
            if user:
                if not user.is_active:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'The user account is disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)

                payload = jwt_payload_handler(user)
                response_data = {
                    'token': jwt_encode_handler(payload)
                }
                return Response(response_data)
        else:
            return Response({
                    'status': 'Bad request',
                    'message': 'Authentication could not be performed with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)

class SocialAuthViewComplete(APIView):
    def post(self, request, backend, *args, **kwargs):
        try:
            #Wrap up  PSA's `complete` method.    
            authentication = complete(request, backend, *args, **kwargs)
        except Exception as e:
            exc = {
                'error': str(e)
            }
            return Response(exc, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': authentication}, status=status.HTTP_202_ACCEPTED)

### TEMPLATES
def index(request):
    return render(request, 'index.html')
def logout(request):
    auth_logout(request)
    return redirect('/v1/temp-social')



## ---------------------   MOD - GESTION      -----------------------------  ##

class LoginManagmentHotel(APIView):
    permission_classes = ()
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            try:
                user = User.objects.get(email = email)
            except User.DoesNotExist:
                return Response({'message': 'No user is associated with this email address' }, status=status.HTTP_404_NOT_FOUND)
        
            if user.tipo_usuario != 'CLIENTE' and user.is_active is True:
                if check_password(password, user.password):
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    return Response({ 'token': token },status=status.HTTP_200_OK)
                return Response({ 'message': 'The password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST) 
            return Response({ 'message': 'You cannot log in with the credentials provided.'}, status=status.HTTP_400_BAD_REQUEST)               
        return Response({ 'message': 'Request could not be performed with received data.'}, status=status.HTTP_400_BAD_REQUEST) 

class CurrentUserView(APIView):
    def get(self, request):        
        serializer = UserDetailSerializers(request.user)
        return Response(serializer.data)

class UserDecodeToken(APIView):
    def get(self,request):
        authorization = request.headers['Authorization']
        token = authorization.split()[1]
        payload = jwt_decode_handler(token)
        user = User.objects.get(pk=payload['user_id'])
        serializer = UserDetailSerializers(user)
        return Response(serializer.data)





















#Vistas para administracion falta actualizar el de update user
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = ([IsOwnerOrAdmin])

    permission_classes_by_action = { 'list': [IsAdmin], 'create':[] }
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def list(self, request, *args , **kwargs):
        self.queryset = User.objects.order_by('id')
        return super(UserViewSet,self).list(request, *args, **kwargs)


    def create(self, request, *args , **kwargs):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password')
        if len(password) < 6:
            return Response({ 'message': 'La contraseña es muy corta. Debe contener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        if password.isalpha()  or password.isdigit() :
            return Response({ 'message': 'La contraseña debe ser alfanumérica.'}, status=status.HTTP_400_BAD_REQUEST)
        if re.search(' ',password)  is not None:
            return Response({ 'message': 'La contraseña no debe contener espacios.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

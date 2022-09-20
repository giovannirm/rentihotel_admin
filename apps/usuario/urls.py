from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import *

#UserViewSet,UserRegistrationView,ConfirmRegistrationView,        ,JwtSocialAuthView,ChangePasswordView,index,logout
#from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

router = DefaultRouter()
#router.register('user',UserViewSet,basename='user_administration')

urlpatterns = [
    path('jwt-auth-social', JwtSocialAuthView.as_view()), 
    
    path('account/login', obtain_jwt_token,name="account_login"),
    path('managment/account/login',LoginManagmentHotel.as_view()),

    path('account/logout',AccountLogoutView.as_view(),name='account_logout'),
    path('account/register', UserRegistrationView.as_view(),name='register_account'), 
    path('account/activate/<str:uidb64>/<str:token>', ConfirmRegistrationView.as_view(), name='activate_account'),
    #path('password/change', ChangePasswordView.as_view()), 
    path('password/reset', ResetPasswordView.as_view(),name='password_reset'),
    path('password/reset/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/<str:uidb64>/<str:token>/done', PasswordResetComplete.as_view(), name='password_reset_complete'),

    path('user/active', CurrentUserView.as_view(), name='current_user'),
    path('user/user' , UserDecodeToken.as_view(), name='user_decode'),
    
    path('temp-social', index, name='redes sociales'),
    path('logout', logout, name='log-out'),  
    
]
urlpatterns += router.urls

#path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
"""somproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

#-------------------media 경로로의 파일 요청을 위함---------------------
from django.conf import settings
from django.conf.urls.static import static
#----------------------------------------------------------------------


urlpatterns = [
    #path('login/', views.login, name='login_frontend' ),
    path('login/', views.login, name='login' ),
    #path('signup/', views.signup, name='signup_frontend'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('auth_kakao/', views.auth_kakao, name="auth_kakao"),   #카카오톡으로 로그인
    path('sendcode/',views.send_code, name='send_code'),        # 인증번호 발송을 위한 URL
    path('verify/',views.verify_code, name='verify_code'),      # 인증번호 검증을 위한 URL
    path('temp_success/', views.temp_success, name='success_backend'),    # 로그인/회원가입 성공을 확인하기 위해 추가한 임시 URL (추후 삭제할 것!)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from django.contrib import admin
from django.urls import path, include
import main.views

##import login.views

#-------------------media 경로로의 파일 요청을 위함---------------------
from django.conf import settings
from django.conf.urls.static import static
#----------------------------------------------------------------------

urlpatterns = [
    path('', main.views.main, name='main'),
    path('admin/', admin.site.urls),
    path('member/', include('member.urls'),),                      # login App URL 을 /member 로 임시 변경
    path('donation/', include('donation.urls',))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

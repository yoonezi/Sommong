from django.urls import path
from . import views

#-------------------media 경로로의 파일 요청을 위함---------------------
from django.conf import settings
from django.conf.urls.static import static
#----------------------------------------------------------------------

urlpatterns = [
    #path('animal_list/', views.animal_list, name='animal_list'),
    #path('animal_list/', views.animal_list, name='animal_list_backend'), ## 동물 상세보기 페이지
    #path('kakaoPay/', views.kakaoPay, name="kakaoPay_backend"),         ## 카카오 결제 요청
    #path('kakaoPay_approval/', views.kakaoPay_approval, name="approval_backend"),         ## 카카오 결제 승인
    #path('kakaoPay_cancel/', views.kakaoPay_cancel, name="kakaoPay_cancel_backend"),
    #path('kakaoPay_fail/', views.kakaoPay_fail, name="kakaoPay_fail_backend"),
    path('reply/', views.reply, name="reply"),
    path('animal_list/', views.front_anim_list, name='front_anim_list'),
    path('animal_detail/', views.front_anim_detail, name='front_anim_detail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

import datetime
import uuid
import os

class som_user_profile(models.Model):            ## User Profile Model
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('imgs/users', filename)

    class AccTypeInProfile(models.TextChoices):
        KAKAO = 'K', _('카카오')                   # 활동 중 (기부 가능 상태)
        GOOGLE = 'G', _('구글')           # 최초 가입 시, 승인 대기 상태 (기부 불가 상태) 
        NAVER = 'N', _('네이버')                   # 자의에 의한 탈퇴 (기부 불가 상태)            = User 들에게 별도로 공지됨
        SOMM = 'S', _('솜뭉')

    user = models.OneToOneField(User, on_delete=models.CASCADE)                    ## User 모델에 대한 외래키
    mb_hp = models.CharField(max_length=20, null=True, unique=True)                           ## 회원 전화번호
    mb_name = models.CharField(max_length=20, null=True)                                      ## 회원 이름
    mb_img = models.ImageField(upload_to=get_file_path, default='imgs/default_user.png')    ## 회원 프로필 사진 (마이 페이지에서 설정토록 함, 회원 가입 시는 필요 없음)
    # upload_to : 이미지 경로
    # 기본 프로필 이미지 : imgs/default_user.png

    mb_nick = models.CharField(max_length=50, blank=True)
    mb_account_type= models.CharField(max_length=1,validators=[MinLengthValidator(1)], choices =AccTypeInProfile.choices)

    ##class VerStateInUser(models.TextChoices):

    def save(self, *args, **kwargs):                                               ## 닉네임 기본값 : 회원 ID 로 하여 저장
        if self.mb_nick=='':           
            self.mb_nick = id = self.user.username
        super(som_user_profile, self).save(*args, **kwargs)


## 현재로썬 보호소 계정의 존재 목적은, 플랫폼 후원 혜택을 받고있는 보호소 및 등록된 사설 보호소의 관리를 용이(플랫폼 내에서 자체적으로 할 수 있도록)하게 하기 위함
## 따라서, 동물 정보 등록, 수정은 플랫폼 관리자가 하는 것으로 정함 (8월 까지는...)

class som_shelter_profile(models.Model):

    class StateInShelter(models.TextChoices):
        ACTV = 'A', _('활동')                   # 활동 중 (기부 가능 상태)
        PEND = 'P', _('승인 대기 중')           # 최초 가입 시, 승인 대기 상태 (기부 불가 상태) 
        QUIT = 'Q', _('탈퇴')                   # 자의에 의한 탈퇴 (기부 불가 상태)            = User 들에게 별도로 공지됨
        BLCK = 'B', _('차단')                   # 플랫폼에서 활동을 차단시킴 (기부 불가 상태)   = User 들에게 별도로 공지됨

    user = models.OneToOneField(User, on_delete=models.CASCADE)        ## User 모델에 대한 외래키    
    shelter_id = models.AutoField(primary_key=True)                    
    shelter_name = models.CharField(max_length=50)                     ## 보호소 이름
    shelter_addr = models.CharField(max_length=100, null=True,blank=True) ## 보호소 주소
    
    ## 일단, 보호소 인증을 위해, 사설 보호소로 직접 연락한다 가정하므로, 담당자 연락처 번호 기입 필수토록!
    shelter_hp = models.CharField(max_length=25)                                                        ## 보호소 전화번호/담당자 연락처
    shelter_link = models.CharField(max_length=45,null=True,blank=True)                                 ## 보호소 홈페이지
    shelter_img = models.ImageField(upload_to='imgs/shelter', default='imgs/default_shelter.png',null=True,blank=True) ## 보호소 프로필 사진
    shelter_valid = models.CharField(max_length=1, choices =StateInShelter.choices, default=StateInShelter.PEND)       ## 보호소 계정 등록 상태
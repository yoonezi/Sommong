from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login


from django.conf import settings
from django.http import JsonResponse   
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

from .utils import *
from .models import *

import json

##----------- 로그인 성공 확인 용 (Main 페이지 구현 시 삭제!) ------------------
def temp_success(request):
    return render(request,'success_backend.html')
##------------------------------------------------------------------------------



## 로그인 기능 완성
def login(request):

    #return render(request,'login_backend.html',{'kakao_key' : settings.KAKAO_OAUTH_KEY})
    #return render(request, 'login.html')        ## Front-End 작업 전용

    ## 아래 코드는, login_backend.html 과 연결된 코드(로그인 완성된 코드)입니다.!
    ## 만일 로그인 기능을 테스트해보고 싶다면, 위의, login.html 로 연결되는 코드를 주석처리하고, 아래의 코드를 주석해제하세요!
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            remember_session = request.POST.get('remember_session')
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            else:
                request.session.set_expiry(0)
                request.session.modified = True
            ##----------- 로그인 성공 테스트 용 (Main 페이지 구현 시 삭제!) ------------------
            return redirect('/')
            ##------------------------------------------------------------------------------
            ## return redirect('/')
        else:
            return render(request, 'login.html',{'error':"사용자 이름 혹은 패스워드가 일치하지 않습니다."})
    return render(request,'login.html',{'kakao_key' : settings.KAKAO_OAUTH_KEY})

## 로그아웃 기능 완성
def logout(request):
    auth.logout(request)
    return redirect('/member/login')

## 회원 가입 기능 미완성
def signup(request):
    #return render(request,'signup.html')           ## Front-End 작업 전용
    #return render(request,'signup_backend.html')  ## Backend-End 작업 전용
    if request.method=="POST":
        user_id = request.POST.get('username')               ## 회원 ID
        user_pw = request.POST.get('password')               ## 비밀번호
        user_pwCheck = request.POST.get('passwordCheck')   ## 비밀번호 확인
        user_name = request.POST.get('mb_name')               ## 회원 실명
        user_email=request.POST.get('email')                     ## 회원 이메일
        user_hp = request.POST.get('mb_hp')                   ## 회원 전화번호

        print(user_id)
        print(user_pw)
        print(user_pwCheck)
        print(user_hp)
        validity = is_valid_info([user_id, user_pw, user_pwCheck, user_name, user_email, user_hp])

        if not validity['status']: 
            return render(request, 'signup.html', {'error':validity['msg']})
        if User.objects.filter(username=user_id).exists():
            return render(request, 'signup.html', {'error':"이미 존재하는 아이디입니다."})
        if som_user_profile.objects.filter(mb_hp = user_hp).exists():
            return render(request, 'signup.html', {'error': '이미 등록된 연락처입니다.'})
        if not is_sms_vrfied(request)['status']:
            return render(request, 'signup.html', {'error': is_sms_vrfied(request)['msg']})

        user = User.objects.create_user(username=user_id, password=user_pw,email=user_email)
        som_profile=som_user_profile()
        som_profile.user=user
        som_profile.mb_hp=user_hp
        som_profile.mb_name=user_name
        som_profile.mb_account_type = 'S'
        
        som_profile.save()
        auth.login(request, user)
        return redirect('/')
    else:
        if 'sms_verify' in request.session:     
            del request.session['sms_verify']
        # 세션에서 모바일 인증 관련 정보 삭제
        return render(request,'signup.html')


## 문자인증 완성
@csrf_exempt  # 임시로, CSRF 토큰 해제 (Front End 에서 Ajax 코드 완성 후, 다시 CSRF 토큰 추가)
def send_code (request):
    if 'sms_verify' in list(request.session.keys()): 
        del request.session['sms_verify']
    # 세션에서 모바일 인증 관련 정보 삭제
    if request.method=="POST":
        data = json.loads(request.body)
        mb_hp = '+82' + data['mb_hp']

        sns_wrapper = SnsWrapper()
        random_code = random_code_generator() 
        request.session['sms_verify'] = {}
        request.session['sms_verify']['sms_code'] = random_code 
        request.session['sms_verify']['expire'] = set_expire()

        template = f'\U0001F436[From 솜뭉]\U0001F436 인증코드는 {random_code} 입니다.'

        try :
            sns_wrapper.publish_text_message(mb_hp, template)
            print('sent success')
        except Exception as e :
            return JsonResponse({'message' : 'Message Send Failed'}, status=500)
        return JsonResponse({'message' : 'OK'}, status=200)
    return JsonResponse({'message' : 'Only POST Allowed'}, status=405)


## 문자인증번호 검증 완성
@csrf_exempt
def verify_code (request):
    if request.method=="POST":
        if 'sms_verify' in list(request.session.keys()):
            vrfy_info = request.session['sms_verify']
            data = json.loads(request.body)
            code = data['mb_code']

            expire = vrfy_info['expire']
            
            if code != vrfy_info['sms_code']:
                return JsonResponse  ({'message' : 'Not Matched'}, status=500)
            if is_expired(expire):
                return JsonResponse  ({'message' : 'Expired'}, status=500) 
            vrfy_info['is_vrfied'] = True
            return JsonResponse({'message' : 'OK'}, status=200)
            
        return JsonResponse({'message' : 'Request Code First'}, status=500)
    return JsonResponse({'message' : 'Only POST Allowed'}, status=405)


## 카카오계정 로그인/가입 완성
@csrf_exempt
def auth_kakao(request):
    if request.method == "POST": 
        obj = json.loads(request.body)
        mb_nick= obj['name']
        username = obj['id']
        pw = hash_sns_pw(mb_nick + username)
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=pw)
            auth.login(request,user)
            return render(request, 'signup.html')   
        else:
            user = User.objects.create_user(username=username, password=pw)  ## (username + mb_nick + secret)key sign == password)
            som_profile=som_user_profile()
            som_profile.user=user
            som_profile.mb_nick=mb_nick
            som_profile.mb_account_type = 'K'
            som_profile.save()
            auth.login(request, user)
            return redirect('/member/login')
    else :
        return render(request, 'signup.html')    



def check_session(request):
    print(request.session.items())
    return JsonResponse({'message' : 'Test!'}, status=200)

import boto3
import string
import datetime

from random import choice
from django.conf import settings
from botocore.exceptions import ClientError
import re
import hashlib

## --------------- soon will be replaced to forms.py ------------------------

def is_sms_vrfied(request):
    if 'sms_verify' not in list(request.session.keys()):
        return {'status': False,'msg': '먼저 문자인증을 하세요.'}
        render(request, 'signup_backend.html', {'error': '먼저 문자인증을 하세요.'})
    if 'is_vrfied' not in list(request.session['sms_verify'].keys()) :
        return {'status' : False, 'msg': '인증번호가 검증되지 않았습니다.'}
    return {'status' : True, 'msg' : '성공'}


def is_valid_info(user_info):
    user_id, user_pw, user_pwCheck, user_name, user_email, user_hp = user_info
    if is_null(user_info):
        return {'status' : False, 'msg' : '모든 값을 입력해주세요.'}
    if is_validID(user_id):
        return {'status' : False, 'msg' : '아이디는 반드시 4~12자 영문/숫자로 구성되어야 합니다.'}
    if is_validPW(user_pw):
        return {'status' : False, 'msg' : '비밀번호는 반드시 10자 이상의 최소하나씩의 영문/숫자/특수문자로 구성되어야 합니다.'}    
    if is_validHP(user_hp):     
        return {'status':False ,'msg': '유효하지 않은 핸드폰 번호 형식입니다.'}
    if user_pw != user_pwCheck :
        return { 'status': False, 'msg': '비밀번호가 일치하지 않습니다.'}
    return {'status': True, 'msg' : '성공'}

def is_validID(user_id):
    patt = re.compile('^[0-9|a-z|A-Z]{4,12}$')
    m = patt.match(user_id)
    return m is None

def is_validPW(user_pw):
    patt = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$')
    m = patt.match(user_pw)
    return m is None

def is_validHP(user_hp):
    patt = re.compile('^\s*(010|011)([0-9]{4}){2}\s*$')
    m = patt.match(user_hp)
    return m is None

def is_null(user_info):
    return None in user_info
## --------------------------------------------------------------------------

def hash_sns_pw (pw):
    result = hashlib.sha256(pw.encode())
    return result.hexdigest()


def is_expired(str_time):
    due = datetime.datetime.strptime(str_time,"%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now().replace(microsecond=0)
    return due < now

def set_expire():
    due = datetime.datetime.now() + datetime.timedelta(seconds=60*3) ## 인증번호는 최대 3분 유효함. 
    return due.strftime("%Y-%m-%d %H:%M:%S")


def random_code_generator():
    randoms =  ''.join(choice(string.digits) for _ in range(6))
    return randoms

class SnsWrapper:                     ## aws sns 사용하여 본인인즌 진행
    def __init__(self):
        sns_api =  boto3.resource(
            'sns', 
            aws_access_key_id = settings.AWS_ACCESS_KEY,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            region_name = settings.REGION_SNS
        )
        self.sns_resource = sns_api

    def publish_text_message(self, phone_number, message):
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
        except ClientError:
            raise
        else:
            return message_id
    



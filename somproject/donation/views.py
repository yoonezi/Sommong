from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator  ## 페이지네이셔닝 기능

from .models import *
from member.models import *
from main.models import *


@csrf_exempt
def animal_list(request):
    if request.method=="GET":
        ## 무한 스크롤은 여기서 구현됨
        category = {
            'shelter' : som_shelter_profile.objects.all(),    ## 등록된 모든 보호소들에 대한 정보
            'breed' : som_anim_category.objects.all(),
            'sex' : {'M' : '수컷','F' : '암컷'},
            'age' : list(range(0,22))
        }

        anim_infos = som_animal.objects.all().order_by('anim_regdate')[:settings.PAGE_OFFSET]    ## 한 페이지 당 36 마리 (6줄)
        return render(request,'animal_list_backend.html', {'anim_infos' : anim_infos, 'category': category})

        ## ajax 사용하여, 카테고리 정보 전달 
        ## 
    
    ## POST 로 전달된 동물 카테고리 (다시 동물 갖고오기)
    
    return render(request,'animal_list_backend.html')
        ## 기본 정렬 : 입소일 순
        ## 동물 카드 보여주기
        ## 보호소/성별/종/나이 카테고리
        ## 보호소 - DB 에 저장된 보호소
        ## 성별 - 수컷, 암컷
        ## 종 - DB 에 저장된 종 정보
        ## 나이 - 0 ~ 20 살 까지
        ## 카드에 표현될 동뭉 이미지는 img1


'''
def kakaoPay(request):
    if request.method == "POST":
        request.get_host()
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + settings.KAKAO_OAUTH_KEY,   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "연어초밥",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "12000",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": "http://sample.cloutype.io:8000/donation/kakaoPay_approval",  ## 결제 승인 시, 이동할 url (배포 시, CloudType.io 도메인 적용)
            "cancel_url": "http://sample.cloutype.io:8000/donation/kakaoPay_cancel",     ## 결제 취소 시, 이동할 url (배포 시, CloudType.io 도메인 적용)
            "fail_url": "http://sample.cloutype.io:8000/donation/kakaoPay_fail",               ## 결제 실패 시, 이동할 url (배포 시, CloudType.io 도메인 적용)
        }
        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)
    return render(request, 'kakaopay_backend.html')


def kakaoPay_approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + settings.KAKAO_OAUTH_KEY,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",      # 주문번호
        "partner_user_id": "german",     # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    res = res.json()
    context = {
        'res': res,
    }
    return render(request, 'pay_approval_backend.html', {'context':context, 'params':params})

def kakaoPay_cancel(request):
    return render(request,'pay_cancel_backend.html')

def kakaoPay_fail(request):
    return render(request, 'pay_fail_backend.html')

'''

def reply(request):
    if request.method == 'POST':
        comm_content = request.POST.get('comm_content')
        mb_id =  som_user_profile.objects.get(pk=int(request.POST.get('mb_id'))) 
        post_id = som_anim_post.objects.get(post_id=int(request.POST.get('post_id')))

        comment = som_anim_comment()
        comment.comm_content = comm_content
        comment.post_id = post_id
        comment.mb_id = mb_id
        comment.save()

        return redirect('/donation/reply')            #이부분 post아니고 다른걸로 수정하면 돼용!
    else:    ## 페이지 로딩
        ## 동물의 ID 를 갖고, Post ID 갖고오기
        comments = som_anim_comment.objects.filter(post_id=1)        
        return render(request, 'reply.html',{'comments' : comments}) # 홈으로




def front_anim_list(request):
    page = request.GET.get('page', '1')  # 페이지
    anim_infos = som_animal.objects.all().order_by('anim_regdate')   ## 한 페이지 당 36 마리 (6줄)
    paginator = Paginator(anim_infos, settings.PAGE_OFFSET)  # 페이지당 12개씩 보여주기
    page_obj = paginator.get_page(page)  ##
    context = {'anim_infos': page_obj}
    return render(request, 'donation_list_backend.html', context)

def front_anim_detail(request):
    return render(request,'donation_detail.html')


'''
def front_anim_list(request):
    ## anim_id =request.GET.get('anim_id')
    ##  som_animal.objects.get(pk=anim_id)
    anim_info =  som_animal.objects.get(pk=1)

    #anim_infos = som_animal.objects.all().order_by('anim_regdate')   ## 한 페이지 당 36 마리 (6줄)
    #paginator = Paginator(anim_infos, settings.PAGE_OFFSET)  # 페이지당 12개씩 보여주기
    #page_obj = paginator.get_page(page)  ##
    context = {'anim': anim_info}
    return render(request, 'donation_detail.html', context)    ## {{ anim.img1_url }} 을 <img> 의 src 속성값으로 전달
    '''
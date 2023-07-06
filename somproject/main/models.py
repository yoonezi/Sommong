from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError
from member.models import *


class som_anim_category(models.Model):
    ca_id = models.AutoField(primary_key=True)
    ca_name1 = models.CharField(max_length=9)
    ca_name2 = models.CharField(max_length=50)

class som_anim_post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_content = models.TextField()


class som_anim_comment(models.Model):
    post_id = models.ForeignKey(som_anim_post, on_delete=models.CASCADE)
    mb_id = models.ForeignKey(som_user_profile, on_delete = models.CASCADE)
    comm_date = models.DateTimeField(auto_now_add=True)
    comm_content = models.TextField(blank=True)



class som_anim_in_state(models.Model):             ## 보호소 내에서 추적/관리가 더이상 불가능 한 동물들 / 미지수인 동물들에 대한 불가능 사유 (보호소에서 제명된 상태) - 특정 동물에 대한 후원 활성화 여부 파악 위함
    class StateInAnim(models.TextChoices):
        DECEASED = 'DCS', _('사망')
        ADOPTED = 'ADP', _('입양')
        ETC = 'ETC', _('기타')                       
                                                     
    ## 후원자들에게, 후원 시, 동물의 사망, 의도치 않은 손/망실이 발생할 수 있고, 이에 대해 현재까진, 플랫폼서 후원금을 반환할 수 없다는 약관 명시
    
    state_id = models.AutoField(primary_key=True)
    state_code = models.CharField(max_length=3, choices=StateInAnim.choices)
    state_regdate = models.DateTimeField(null=False, blank=False,auto_now_add=True)
    extra_field1 = models.CharField(max_length=50,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.state_code==StateInAnim.ETC and self.extra_field1.strip() =='':
            raise ValidationError("반드시 제명 사유를 명시해주셔야합니다.", code='field-tempty')      
        super(som_anim_in_state, self).save(*args, **kwargs)





class som_animal(models.Model):

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('imgs/animal', filename)

    class SexInAnim(models.TextChoices):
        MALE = 'M', _('수컷')
        FEMALE = 'F', _('암컷')

    class NeuterInAnim(models.TextChoices):
        NEUTER = 'NE', _('중성화')
        INTACT = 'IN', _('비중성화')

    anim_id = models.AutoField(primary_key=True)                   
    anim_code = models.CharField(max_length=50, null = True)      
    ## 사설 보호소의 경우, 공고번호가 없는 유기동물 존재 (사설 보호소의 경우, 공고기간이 지난 유기동물을 입양받아오는 경우가 대다수)
    ## 따라서, 공고번호가 있는 동물과 없는 동물이 보호소 내에 있을 수 있다는 사실 고려
    anim_name = models.CharField(max_length=100)
    anim_sex = models.CharField(max_length=1,choices=SexInAnim.choices)
    anim_breed = models.ForeignKey(som_anim_category, on_delete = models.CASCADE)
    anim_regdate = models.DateField(null=False, blank=False,auto_now_add=True)
    anim_weight = models.DecimalField(max_digits=3,decimal_places=1,validators=[MinValueValidator(0.0)])   
    anim_age = models.IntegerField(validators=[MinValueValidator(0)])
    anim_found = models.CharField(max_length=100)
    anim_post_id = models.ForeignKey(som_anim_post, null=True,blank=True, on_delete=models.PROTECT)
    ## 게시글의 경우, 동물과 1:1 대응이긴 하나, 동물의 정보를 먼저 올리고, 게시글을 올리기에, nullable 속성 부여
    anim_neuter = models.CharField(max_length=2,choices =NeuterInAnim.choices)
    shelter_id = models.ForeignKey(som_shelter_profile, on_delete=models.PROTECT)
    in_state_id = models.ForeignKey(som_anim_in_state, null = True, on_delete = models.PROTECT, blank=True)

    anim_img1 = models.ImageField( upload_to=get_file_path) 
    ## 최소 해당 동물의 사진 한장 정도는 올리도록 설정
    anim_img2 = models.ImageField( upload_to=get_file_path, null=True, blank=True)           # 여분 이미지 필드
    anim_img3 = models.ImageField( upload_to=get_file_path, null=True, blank=True)
    anim_img4 = models.ImageField(upload_to=get_file_path, null=True, blank=True)

    #동물 별도에 대한 입소 상태 (입양 - 후원 불가, 사망 - 후원 불가) 
    # 후원이 중간에 불가능하게 되는 경우, 반드시 보호소로부터 사유를 받도록 함.


    DEFAULT_CAT_NAME = '냥이'
    DEFAULT_DOG_NAME = '강아지'


    def save(self, *args, **kwargs):
        if self.anim_name=='':           
            if som_anim_category.objects.filter(ca_id=self.anim_breed) == '개':
                self.anim_name = DEFAULT_DOG_NAME
            if som_anim_category.objects.filter(ca_id=self.anim_breed) == '고양이':
                self.anim_name = DEFAULT_CAT_NAME
        super(som_animal, self).save(*args, **kwargs)




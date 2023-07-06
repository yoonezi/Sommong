from django.db import models

# Create your models here.
from main.models import *
from member.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

'''
class som_favlist(models.Model):
    fav_id = models.AutoField(primary_key=True)
    anim_id = models.ForeignKey(som_animal,on_delete=models.CASCADE)
    mb_id = models.ForeignKey(som_profile, on_delete = models.CASCADE)


class som_donation_item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_type = models.IntegerField(validators=[MinValueValidator(0)])
    item_price = models.IntegerField(validators=[MinValueValidator(0)])
    item_img = models.ImageField(upload_to='imgs/item', default='imgs/default_item.png', null= True)
    item_link =models.CharField(max_length=45)
    # 사료, 간식, 배변 패드/모래, 기타(옷/신발/... 비소모품)

class som_payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    mb_id = models.ForeignKey(som_profile, on_delete = models.CASCADE)
    anim_id = models.ForeignKey(som_animal, on_delete = models.CASCADE)

class som_goods_payment_detail(models.Model):
    goods_payment_detail_id = models.AutoField(primary_key=True)
    payment_id = models.ForeignKey(som_payment, on_delete = models.CASCADE)
    item_id = models.ForeignKey(som_donation_item, on_delete = models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    count = models.IntegerField(validators=[MinValueValidator(0)])


class som_pay_financial_detail(models.Model):
    financial_detail_id = models.AutoField(primary_key=True)
    payment_id = models.ForeignKey(som_payment, on_delete = models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    '''
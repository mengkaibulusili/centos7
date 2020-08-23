# from django.shortcuts import render
# from django.http import response
import json
from goods import models as goodmodel
from scriptTools import mydecorator
from django.db import transaction


# Create your views here.
@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


# 1. 创建品牌
# 2. 修改品牌
# 2. 创建商品
# 3. 修改商品


# brandname
# brandtelephone
# brandaddress
# http://127.0.0.1:8000/api/goods/createBrand/?data={"brandname": "海飞丝","brandtelephone":"1122","brandaddress":"鹤壁"}
@mydecorator.httpRes
def createBrand(request):
  data_dict = json.loads(request.GET.get("data"))
  goodmodel.GoodsBand(**data_dict).save()


# http://127.0.0.1:8000/api/goods/changeBrand/?data={"oldbrandname":"海飞丝", "brandname": "海飞丝1","brandtelephone":"1122","brandaddress":"鹤壁","state":"可用"}
@mydecorator.httpRes
def changeBrand(request):
  data_dict = json.loads(request.GET.get("data"))
  with transaction.atomic():
    oldbrandname = data_dict.pop("oldbrandname")
    goodmodel.GoodsBand.objects.get(brandname=oldbrandname).delete()
    goodmodel.GoodsBand(**data_dict).save()


# http://127.0.0.1:8000/api/goods/createGood/?data={"brandname": "海飞丝","goodname":"212","goodprice":"2012012","goodintroduce":"as"}
@mydecorator.httpRes
def createGood(request):
  data_dict = json.loads(request.GET.get("data"))
  goodmodel.GoodsInfo(**data_dict).save()


# http://127.0.0.1:8000/api/goods/changeGood/?data={"oldgoodname":"212","goodname":"洗发露","goodprice":"2012012","goodintroduce":"as","state":"下架","brandname": "海飞丝"}
@mydecorator.httpRes
def changeGood(request):
  data_dict = json.loads(request.GET.get("data"))
  with transaction.atomic():
    oldgoodname = data_dict.pop("oldgoodname")
    goodmodel.GoodsInfo.objects.get(goodname=oldgoodname).delete()
    goodmodel.GoodsInfo(**data_dict).save()
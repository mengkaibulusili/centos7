# from django.shortcuts import render
from scriptTools import mydecorator
import json
from projs import models as projmodel
from django.db import transaction
from django.core import serializers


# Create your views here.
def usefucbyname(request, fucname):
  return eval(fucname)(request)


#  功能
# 1.创建项目
# 2.修改项目


# # 可修改
# state
# projintroduce = models.CharField("projintroduce", default="未填写", blank=True, max_length=charlen)
# # 必填
# projname = models.CharField("projname", unique=True, max_length=charlen)
# projprice = models.CharField("projprice", max_length=charlen)
# http://127.0.0.1:8000/api/projs/createProj/?data={"projname": "海飞丝","projprice":"212","projintroduce":"2012012"}
@mydecorator.httpRes
def createProj(request):
  data_dict = json.loads(request.GET.get("data"))
  projmodel.ProjInfo(**data_dict).save()


# http://127.0.0.1:8000/api/projs/changeProj/?data={"oldprojname":"海飞丝","projname": "海飞丝","projprice":"212","projintroduce":"2012012","state":"下架"}
@mydecorator.httpRes
def changeProj(request):
  data_dict = json.loads(request.GET.get("data"))
  with transaction.atomic():
    oldprojname = data_dict.pop("oldprojname")
    projmodel.ProjInfo.objects.get(projname=oldprojname).delete()
    projmodel.ProjInfo(**data_dict).save()


# http://127.0.0.1:8000/api/projs/getAllproj
@mydecorator.httpData
def getAllProj(request):
  return json.loads(serializers.serialize("json", projmodel.ProjInfo.objects.all().order_by("-createtime")))

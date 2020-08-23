# from django.shortcuts import render
from django.core import serializers
from django.db import transaction
import vips.models as vipmodel
import staffs.models as staffmodel
# from django.shortcuts import HttpResponse
import json
from scriptTools import mydecorator
from scriptTools import timeTools as tTools

# 序列化数据库数据
# python manage.py shell
# from django.core import serializers
# data = serializers.serialize("json", vips.VipsInfo.objects.all(), fields=("name","tele"))


# Create your views here.
@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


# 功能
# 1.创建 vip
# 2.vip 充值
# 3.vip 购买 项目
# 4.vip 真正到店使用 项目

# 5.vip 下单购买 产品
# 6.给 vip 发送产品


def subRemainMoney(viptelephone, consumemoney):
  x = vipmodel.VipsInfo.objects.get(telephone=viptelephone)
  if float(x.remainmoney) >= float(consumemoney):
    x.remainmoney = str(float(x.remainmoney) - float(consumemoney))
    x.save()
    return True
  return False


#  http://127.0.0.1:8000/api/vips/createVip?data={"name": "kiki", "telephone": "1232112", "birthday": "198902", "staffid": "1", "staff": "keke"}
@mydecorator.httpRes
def createVip(request):
  vip_info_json = request.GET.get("data")
  vip_dict = json.loads(vip_info_json)
  vipmodel.VipsInfo(**vip_dict).save()


# vip 充值 ,
#  http://127.0.0.1:8000/api/vips/vipRechange?data={"vipname": "kiki", "viptelephone": "1232112", "rechangemoney": "198902", "staffid": "2asa-1212", "staff": "keke"}
@mydecorator.httpData
def vipRechange(request):
  rechange_info_json = request.GET.get("data")
  rechange_dict = json.loads(rechange_info_json)
  with transaction.atomic():
    vipmodel.VipsRechange(**rechange_dict).save()
    x = vipmodel.VipsInfo.objects.get(telephone=rechange_dict["viptelephone"])
    x.summoney = str(float(x.summoney) + float(rechange_dict["rechangemoney"]))
    resdata = {"old_r": x.remainmoney, "add_r": rechange_dict["rechangemoney"]}
    x.remainmoney = str(float(x.remainmoney) + float(rechange_dict["rechangemoney"]))
    x.save()
    resdata["new_r"] = x.remainmoney
    y = staffmodel.StaffsInfo.objects.get(staffid=rechange_dict["staffid"])
    y.totalturnover = str(float(y.totalturnover) + float(rechange_dict["rechangemoney"]))
    y.save()
  return resdata


# vip 购买项目
#  http://127.0.0.1:8000/api/vips/buyProjs?data={"times":"3","vipname": "kiki", "viptelephone": "1232112", "projid": "198902", "projname": "跑步", "projprice": "10", "staffid": "2asa-1212", "staff": "keke"}
@mydecorator.httpData
def buyProjs(request):
  resData = {}
  proj_info_json = request.GET.get("data")
  proj_dict = json.loads(proj_info_json)
  # 购买次数
  times = int(proj_dict["times"])
  proj_dict.pop("times")
  viptelephone = proj_dict["viptelephone"]
  with transaction.atomic():
    if subRemainMoney(viptelephone, times * float(proj_dict["projprice"])):
      for x in range(times):
        vipmodel.VipsProj(**proj_dict).save()
      resData["info"] = "购买成功"
    else:
      resData["info"] = "余额不足"
  resData["remain_money"] = vipmodel.VipsInfo.objects.get(telephone=viptelephone).remainmoney
  return resData


# vip 到店真正使用项目
# http://127.0.0.1:8000/api/vips/useProj?vipprojid=2
@mydecorator.httpRes
def useProj(request):
  vipprojid = request.GET.get("vipprojid")
  x = vipmodel.VipsProj.objects.get(vipprojid=vipprojid)
  x.state = "完成"
  x.usetime = tTools.dateStdTime()
  x.save()


@mydecorator.httpData
def cancelBuyProj(request):
  resData = {}
  resData["info"] = "取消失败"
  vipprojid = request.GET.get("vipprojid")
  with transaction.atomic():
    x = vipmodel.VipsProj.objects.get(vipprojid=vipprojid)
    if ("未使用" == x.state) or ("完成" == x.state):
      x.state = "交易取消"
      x.sendtime = tTools.dateStdTime()
      x.save()
      y = vipmodel.VipsInfo.objects.get(telephone=x.viptelephone)
      y.remainmoney = str(float(y.remainmoney) + float(x.projprice))
      y.save()
      resData["info"] = "交易取消成功"
    elif ("交易取消" == x.state):
      resData["info"] = "交易已经被取消"
  return resData


# 查询某个vip的 已购买项目
# http://127.0.0.1:8000/api/vips/getOneVipProjs?viptelephone=1232112
@mydecorator.httpData
def getOneVipProjs(request):
  viptelephone = request.GET.get("viptelephone")
  return json.loads(serializers.serialize("json", vipmodel.VipsProj.objects.filter(viptelephone=viptelephone)))


# 购买产品
#  http://127.0.0.1:8000/api/vips/buyGoods?data={"count":"5","vipname": "kiki", "viptelephone": "1232112", "goodid": "198902", "goodname": "游泳圈", "goodprice": "999", "staffid": "1", "staff": "keke"}
@mydecorator.httpData
def buyGoods(request):
  resData = {}
  good_info_json = request.GET.get("data")
  good_dict = json.loads(good_info_json)
  # 购买次数
  count = int(good_dict["count"])
  good_dict.pop("count")
  viptelephone = good_dict["viptelephone"]
  with transaction.atomic():
    if subRemainMoney(viptelephone, count * float(good_dict["goodprice"])):
      for x in range(count):
        vipmodel.VipsGood(**good_dict).save()
      resData["info"] = "购买成功"
    else:
      resData["info"] = "余额不足"
  resData["remain_money"] = vipmodel.VipsInfo.objects.get(telephone=viptelephone).remainmoney
  return resData


# 退款退货
# 根据商品交易单号 或者 项目交易单号
# http://127.0.0.1:8000/api/vips/cancelBuyGoods?vipgoodid=1
@mydecorator.httpData
def cancelBuyGood(request):
  resData = {}
  resData["info"] = "取消失败"
  vipgoodid = request.GET.get("vipgoodid")
  with transaction.atomic():
    x = vipmodel.VipsGood.objects.get(vipgoodid=vipgoodid)
    if ("未发货" == x.state) or ("完成" == x.state):
      x.state = "交易取消"
      x.sendtime = tTools.dateStdTime()
      x.save()
      y = vipmodel.VipsInfo.objects.get(telephone=x.viptelephone)
      y.remainmoney = str(float(y.remainmoney) + float(x.goodprice))
      y.save()
      resData["info"] = "交易取消成功"
    elif ("交易取消" == x.state):
      resData["info"] = "交易已经被取消"
  return resData


# 查询某个vip的 已购买商品
# http://127.0.0.1:8000/api/vips/getOneVipGoods?viptelephone=1232112
@mydecorator.httpData
def getOneVipGoods(request):
  viptelephone = request.GET.get("viptelephone")
  return json.loads(serializers.serialize("json", vipmodel.VipsGood.objects.filter(viptelephone=viptelephone)))
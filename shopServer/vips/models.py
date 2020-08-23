from django.db import models
import uuid
import scriptTools.timeTools as tTools

charlen = 50


# Create your models here.
# 新增会员
class VipsInfo(models.Model):
  vipid = models.AutoField("vipid", primary_key=True, auto_created=True)
  vipuuid = models.CharField("vipuuid", default=uuid.uuid1, blank=True, max_length=charlen)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)
  summoney = models.CharField("summoney", default="0", max_length=charlen)
  remainmoney = models.CharField("remainmoney", default="0", max_length=charlen)

  name = models.CharField("name", max_length=charlen)
  telephone = models.CharField("telephone", unique=True, max_length=charlen)
  birthday = models.CharField("birthday", max_length=charlen)
  staffid = models.CharField("staffid", max_length=charlen)
  staff = models.CharField("staff", max_length=charlen)


# 新购项目
class VipsProj(models.Model):
  # 自动初始化的字段
  vipprojid = models.AutoField("vipprojid", primary_key=True)
  vipprojuuid = models.CharField("vipprojuuid", default=uuid.uuid1, blank=True, max_length=charlen)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)

  # 需要后续改动的 字段
  state = models.CharField("state", default="未使用", max_length=charlen, blank=True)
  usetime = models.CharField("usetime", default="-1", max_length=charlen, blank=True)

  # 必须传入的字段
  vipname = models.CharField("vipname", max_length=charlen)
  viptelephone = models.CharField("viptelephone", max_length=charlen)
  projid = models.CharField("projid", max_length=charlen)
  projname = models.CharField("projname", max_length=charlen)
  projprice = models.CharField("projprice", max_length=charlen)
  staffid = models.CharField("staffid", max_length=charlen)
  staff = models.CharField("staff", max_length=charlen)


# 新增购物
class VipsGood(models.Model):
  vipgoodid = models.AutoField("vipgoodid", primary_key=True)
  vipgooduuid = models.CharField("vipgooduuid", default=uuid.uuid1, blank=True, max_length=charlen)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)

  # 需要后续改动的 字段
  state = models.CharField("state", default="未发货", max_length=charlen, blank=True)
  sendtime = models.CharField("sendtime", default="-1", max_length=charlen, blank=True)

  # sp  的 uuid
  vipname = models.CharField("vipname", max_length=charlen)
  viptelephone = models.CharField("viptelephone", max_length=charlen)
  goodid = models.CharField("goodid", max_length=charlen)
  goodname = models.CharField("goodname", max_length=charlen)
  goodprice = models.CharField("goodprice", max_length=charlen)
  staffid = models.CharField("staffid", max_length=charlen)
  staff = models.CharField("staff", max_length=charlen)


# 会员充值
class VipsRechange(models.Model):
  viprechangeid = models.AutoField("viprechangeid", primary_key=True, auto_created=True)
  viprechangeuuid = models.CharField("viprechangeuuid", default=uuid.uuid1, blank=True, max_length=charlen)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)

  # 必须传入的字段
  vipname = models.CharField("vipname", max_length=charlen)
  viptelephone = models.CharField("viptelephone", max_length=charlen)
  rechangemoney = models.CharField("rechangemoney", max_length=charlen)
  staffid = models.CharField("staffid", max_length=charlen)
  staff = models.CharField("staff", max_length=charlen)


# python manage.py shell
# import vips.models as vips
# from django.core import serializers
# data = serializers.serialize('json', vips.VipsInfo.objects.all(), fields=('name','tele'))

# 存储数据
# x1=vips.VipsInfo(name="kiki",telephone="1212",birthday="129",rechangetype="sp",remainmoney="100",summoney="1222",staff="keke")
#  x1.save()
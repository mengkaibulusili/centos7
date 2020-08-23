from django.db import models
from scriptTools import timeTools as tTools

charlen = 50


# Create your models here.
class GoodsInfo(models.Model):
  # 自动生成
  goodid = models.AutoField("goodid", primary_key=True)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)

  # 可修改
  state = models.CharField("state", default="在售", blank=True, max_length=charlen)
  brandname = models.CharField("brandname", default="未填写", blank=True, max_length=charlen)
  goodintroduce = models.CharField("goodintroduce", default="", blank=True, max_length=charlen)

  # 必填
  goodname = models.CharField("goodname", unique=True, max_length=charlen)
  goodprice = models.CharField("goodprice", max_length=charlen)


class GoodsBand(models.Model):
  # 自动生成
  brandid = models.AutoField("brandid", primary_key=True)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)

  # 可修改
  state = models.CharField("state", default="可用", blank=True, max_length=charlen)
  brandaddress = models.CharField("brandaddress", default="未填写", blank=True, max_length=charlen)
  brandtelephone = models.CharField("brandtelephone", default="未填写", blank=True, max_length=charlen)

  # 必填写
  brandname = models.CharField("brandname", unique=True, max_length=charlen)

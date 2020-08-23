from django.db import models
from scriptTools import timeTools as tTools
charlen = 50


# Create your models here.
class ProjInfo(models.Model):
  # 自动生成
  projid = models.AutoField("proid", primary_key=True)
  createtime = models.CharField("createtime", default=tTools.dateStdTime, max_length=charlen, blank=True)
  # 可修改
  state = models.CharField("state", default="在售", blank=True, max_length=charlen)
  projintroduce = models.CharField("projintroduce", default="未填写", blank=True, max_length=charlen)
  # 必填
  projname = models.CharField("projname", unique=True, max_length=charlen)
  projprice = models.CharField("projprice", max_length=charlen)

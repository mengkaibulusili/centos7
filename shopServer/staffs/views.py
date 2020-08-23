import json
# from django.shortcuts import HttpResponse
from staffs import models as staffmodel
from django.core import serializers
import scriptTools.timeTools as tTools
import scriptTools.mydecorator as mydecorator

# data = serializers.serialize("json", vips.VipsInfo.objects.all(), fields=("name","tele"))

# 功能清单
# 创建新员工
# 查询所有员工所有信息
# 修改员工销售额
# 修改员工拉新顾客数目


# Create your views here.
@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


# staffname  stafftelephone  staffbirthday
# http://127.0.0.1:8000/api/staffs/createStaff?data={"staffname": "kiki", "stafftelephone": "1232112", "staffbirthday": "198902"}
@mydecorator.httpRes
def createStaff(request):
  staff_info_json = request.GET.get("data")
  staff_dict = json.loads(staff_info_json)
  staffmodel.StaffsInfo(**staff_dict).save()


# http://127.0.0.1:8000/api/staffs/showStaffs/
@mydecorator.httpData
def showStaffs(request):
  return json.loads(serializers.serialize("json", staffmodel.StaffsInfo.objects.all()))


# http://127.0.0.1:8000/api/staffs/justShowStaffsNameAndId/
@mydecorator.httpData
def justShowStaffsNameAndId(request):
  return json.loads(serializers.serialize("json", staffmodel.StaffsInfo.objects.filter(state="在职"), fields=("staffname")))


# http://127.0.0.1:8000/api/staffs/staffQuit/?data=
@mydecorator.httpRes
def staffQuit(request):
  x = staffmodel.StaffsInfo.objects.get(staffid=request.GET.get("data"))
  x.state = "离职"
  x.quittime = tTools.dateStdTime()
  x.save()


# 修改这个员工的销售额
# staffid and add turnover
# http://127.0.0.1:8000/api/staffs/updateTurnover/?data={"staffid": "2", "turnover": "100"}
@mydecorator.httpData
def updateTurnover(request):
  data_dict = json.loads(request.GET.get("data"))
  x = staffmodel.StaffsInfo.objects.get(staffid=data_dict["staffid"])
  resdata = {"old_t": x.totalturnover, "add_t": data_dict["turnover"]}
  x.totalturnover = str(float(x.totalturnover) + float(data_dict["turnover"]))
  x.save()
  resdata["new_t"] = x.totalturnover
  return resdata


# 修改这个员工拉来的新顾客数量
# staffid
# http://127.0.0.1:8000/api/staffs/updateVip/?data={"staffid": "2"}
@mydecorator.httpData
def updateVip(request):
  data_dict = json.loads(request.GET.get("data"))
  x = staffmodel.StaffsInfo.objects.get(staffid=data_dict["staffid"])
  resdata = {"old_v": x.totalvip, "add_v": "1"}
  x.totalvip = str(int(x.totalvip) + 1)
  x.save()
  resdata["new_v"] = x.totalvip
  return resdata


# 修改这个员工基本薪资
# staffid  salary
# http://127.0.0.1:8000/api/staffs/updateSalary/?data={"staffid": "2","salary":"1000"}
@mydecorator.httpData
def updateSalary(request):
  data_dict = json.loads(request.GET.get("data"))
  x = staffmodel.StaffsInfo.objects.get(staffid=data_dict["staffid"])
  resdata = {"old_s": x.salary, "new_s": data_dict["salary"]}
  x.salary = data_dict["salary"]
  x.save()
  return resdata
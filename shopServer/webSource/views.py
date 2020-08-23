from django.shortcuts import render

# Create your views here.


# Register your models here.
def index(request):
  return render(request, "index.html")

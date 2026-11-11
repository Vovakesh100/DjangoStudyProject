from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'main/index.html')
# return HttpResponse("Hello, world. You're at the polls index.")


def new(request):
    return render(request, 'main/new.html')

# return HttpResponse("hi. You're at the polls index.")
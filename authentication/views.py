from django.shortcuts import render
from django.http import HttpResponse
from .tasks import *

# Create your views here.


def TestView(request):
    test2.delay(10)
    return HttpResponse("hello")


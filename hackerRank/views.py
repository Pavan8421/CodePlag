from django.shortcuts import render
from .models import Submissions
from .hackerRankSelenium import *

# Create your views here.

def index(request):
  hacker = HackerRankSession("pavankumarvaranasi2004@gmail.com","Pavan222")
  hacker.fetch_data("contests/scavenger-hunt-7/judge/submissions")
  return "<h1>Hello</h1>"


def delete(request):
  Submissions.objects.all().delete()
  row_count = Submissions.objects.count()
  if row_count == 0:
    print("Data deleted sucessfully..")
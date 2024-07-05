from itertools import combinations
from django.http import HttpResponse
from django.shortcuts import render
from .models import Submissions,Results
from .hackerRankSelenium import *
from .uploadToMoss import *
import tempfile
import os

# Create your views here.

def index(request):
  hacker = HackerRankSession("pavankumarvaranasi2004@gmail.com","Pavan222")
  hacker.fetch_data("contests/scavenger-hunt-7/judge/submissions")
  load_data()
  return HttpResponse("Hello world")


def generate_combinations(probName, values_list):
    # Filter rows where probName matches and value is in values_list
    rows = list(Submissions.objects.filter(problemName=probName, lang__in=values_list))
    # Generate combinations of 2 rows
    comb = list(combinations(rows, 2))
    return comb

def load_data(request):
  hacker = HackerRankSession("pavankumarvaranasi2004@gmail.com","Pavan222")
  unique_problems = list(Submissions.objects.values_list('problemName',flat=True).distinct())
  print(unique_problems)
  for prob in unique_problems:
    c_lang_submissions = generate_combinations(prob,['c']) #contains pairs of submissions in c lang
    cpp_lang_submissions = generate_combinations(prob,['cpp','cpp14','cpp20']) #contains pairs of submissions in cpp lang
    java_lang_submissions = generate_combinations(prob,['java','java18'])
    python_lang_submissions = generate_combinations(prob,['python2','python3'])
    if(len(c_lang_submissions)):
      fetch_code_into_file("c",c_lang_submissions,hacker)
    if(len(cpp_lang_submissions)):
      fetch_code_into_file("cpp",cpp_lang_submissions,hacker)
    if(len(java_lang_submissions)):
      fetch_code_into_file("java",java_lang_submissions,hacker)
    if(len(python_lang_submissions)):
      fetch_code_into_file("python",python_lang_submissions,hacker)
    break
  #print(unique_problems)
  return HttpResponse('data loaded successfully')


def fetch_code_into_file(lang,code_submissions,hacker):
  for sub in code_submissions:
    code_link1 = sub[0].srcLink
    code_link2 = sub[1].srcLink
    code1 = hacker.fetch_code(code_link1)
    code2 = hacker.fetch_code(code_link2)
    tempfile1 = create_temp_file(lang,code1)
    tempfile2 = create_temp_file(lang,code2)
  return


def create_temp_file(lang, code):
    # Determine the file extension based on the language
    extension = {
        'python': '.py',
        'java': '.java',
        'cpp': '.cpp',
        'c': '.c',
        'javascript': '.js',
        'ruby': '.rb',
        'go': '.go',
    }.get(lang.lower(), '')

    # Get the current directory and create a "temp" directory if it doesn't exist
    current_directory = os.getcwd()
    temp_directory = os.path.join(current_directory, 'temp')
    os.makedirs(temp_directory, exist_ok=True)

    # Create a temporary file in the "temp" directory with the appropriate extension
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode='w', dir=temp_directory) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    print(f"Temporary file created at: {temp_file_path}")
    return temp_file_path


def delete(request):
  Submissions.objects.all().delete()
  row_count = Submissions.objects.count()
  if row_count == 0:
    print("Data deleted sucessfully..")
  return HttpResponse("Data deleted successfully")
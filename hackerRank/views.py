from itertools import combinations
from django.http import HttpResponse
from django.shortcuts import render
from .models import Submissions,Results
from .hackerRankSelenium import *
from .uploadToMoss import *
import tempfile
import os
from hackerRank.models import Results

from sentence_transformers import SentenceTransformer,util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Create your views here.

def index(request):
  return render(request, 'index.html')


def submit(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    contest_slug = request.POST.get('contest_slug')
    hacker = HackerRankSession(username,password)
    hacker.fetch_data(f"contests/{contest_slug}/judge/submissions")
    load_data(username,password, hacker)
    data = Results.objects.all().order_by('-matchPercentage')
    return render(request, 'index.html')
  return HttpResponse("Hello world")


def generate_combinations(probName, values_list):
    # Filter rows where probName matches and value is in values_list
    rows = list(Submissions.objects.filter(problemName=probName, lang__in=values_list))
    # Generate combinations of 2 rows
    comb = list(combinations(rows, 2))
    return comb

def load_data(username,password, hacker):
  #hacker = HackerRankSession(username,password)
  unique_problems = list(Submissions.objects.values_list('problemName',flat=True).distinct())
  print(unique_problems)
  for prob in unique_problems:
    c_lang_submissions = generate_combinations(prob,['c']) #contains pairs of submissions in c lang
    cpp_lang_submissions = generate_combinations(prob,['cpp','cpp14','cpp20']) #contains pairs of submissions in cpp lang
    java_lang_submissions = generate_combinations(prob,['java','java18'])
    python_lang_submissions = generate_combinations(prob,['python2','python3'])
    if(len(c_lang_submissions)):
      get_matchPercentage("c",c_lang_submissions,hacker)
    if(len(cpp_lang_submissions)):
      get_matchPercentage("cpp",cpp_lang_submissions,hacker)
    if(len(java_lang_submissions)):
      get_matchPercentage("java",java_lang_submissions,hacker)
    if(len(python_lang_submissions)):
      get_matchPercentage("python",python_lang_submissions,hacker)
  delete_sub = delete()
  if delete_sub:
    print("Submissions deleted successfully....")
  else:
    print("Submissions not deleted....")
  #print(unique_problems)
  return HttpResponse('data loaded successfully')


def get_matchPercentage(lang,code_submissions,hacker):
  langcode = {
      'c':'c',
      'cpp':'cc',
      'java':'java',
      'python':'python'
  }

  for sub in code_submissions:
    code_link1 = sub[0].srcLink
    code_link2 = sub[1].srcLink
    code1 = hacker.fetch_code(code_link1)
    code2 = hacker.fetch_code(code_link2)
    '''tempfile1 = create_temp_file(lang,code1)
    tempfile2 = create_temp_file(lang,code2)
    percentage = get_similarity_percentage([tempfile1,tempfile2],langcode[lang])'''
    embedding1 = model.encode(code1)
    embedding2 = model.encode(code2)
    sim_Score = util.pytorch_cos_sim(embedding1, embedding2).item()*100
    print(sub[0].problemName , sub[0].username, sub[1].username, sub[0].lang, sim_Score)
    res = Results.objects.create(problemName = str(sub[0].problemName),username1 = str(sub[0].username),username2 = str(sub[1].username),submissionId1 = str(sub[0].submissionId),submissionId2 = str(sub[1].submissionId),lang = str(sub[0].lang), matchPercentage = sim_Score)
    if res:
      print("Row inserted successfully..")
  return


'''def create_temp_file(lang, code):
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
    temp_directory = os.path.join(f"{current_directory}/hackerRank", 'temp')
    os.makedirs(temp_directory, exist_ok=True)

    # Create a temporary file in the "temp" directory with the appropriate extension
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode='w', dir=temp_directory) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    print(f"Temporary file created at: {temp_file_path}")
    return temp_file_path
'''

def delete():
  Submissions.objects.all().delete()
  row_count = Submissions.objects.count()
  if row_count == 0:
    print("Data deleted sucessfully..")
    return True
  return False
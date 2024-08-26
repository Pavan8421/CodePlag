from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

from hackerRank.models import Submissions

path = "F:\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"


#username = "pavankumarvaranasi2004@gmail.com"
#password = "Pavan222"


class HackerRankSession:

  service = Service(path)
  browser = webdriver.Chrome(service=service)
  chrome_options = Options()
  chrome_options.add_argument("--log-level=3")
  chrome_options.add_argument("--disable-blink-features=FirstPaint")

  def __init__(self,username,password):
    self.browser.get("https://www.hackerrank.com/auth/login")
    sleep(10)
    username_input = self.browser.find_element(By.XPATH, "//input[@name='username']")
    password_input = self.browser.find_element(By.XPATH,"//input[@name='password']")
    username_input.send_keys(username)
    password_input.send_keys(password)
    sleep(2)
    login_btn = self.browser.find_element(By.CSS_SELECTOR,".c-cUYkx-dshqME-variant-primary")
    login_btn.click()
    sleep(3)
    print("Login successfull")

  def fetch_link(self, link):
    if link.startswith("http"):
        pass
    else:
        link = f"https://www.hackerrank.com/{link[1:] if link.startswith('/') else link}"
    self.browser.get(link)
    print("Fetched link successfully")
    sleep(5)

  def check_page_valid(self,page,url):
    """
    Fetch an anticipated page in submissions.
    return true if page exists else return false
    """
    url = url+f"/{page}"
    self.fetch_link(url)
    try:
        if self.browser.find_element(By.XPATH, '//div[@class="padding-large top"]/p[@class="text-center" and contains(text(), "There are no submissions.")]'):
          return False
    except Exception as e:
        return True
        #  selenium.common.exceptions.NoSuchElementException
    return True
  
  def fetch_code(self, src_link):
    """
    fetches the source code
    """
    self.fetch_link(src_link)
    code_elements = self.browser.find_elements(
        "class name", "CodeMirror-line")
    return "\n".join([line.text for line in code_elements])

  def fetch_data(self,link):
    page = 1
    while(self.check_page_valid(page,link)):
      # Find all the rows within the main div
      main_div = self.browser.find_elements(By.CLASS_NAME, 'judge-submissions-list-view') #
      for main in main_div:
        submission_items = main.find_elements(By.CLASS_NAME, 'submissions_item')
        # Loop through each submission item and extract data
        for item in submission_items:
            # Extract the problem name
            problem_name = item.find_element(By.XPATH, './/div[@class="span2 submissions-title"]/p/a').text
            #print('Problem Name:', problem_name)
            
            # Extract the username
            username = item.find_element(By.XPATH, './/div[@class="span2 submissions-title"][2]/p/a').text
            #print('Username:', username)
            
            # Extract the submission ID
            submission_id = item.find_element(By.XPATH, './/div[@class="span1 submissions-title"]/p').text
            #print('Submission Id:', submission_id)
            
            # Extract the language used
            language = item.find_element(By.XPATH, './/div[@class="span2 submissions-title"]/p[@class="small"]').text
            #print('Language:', language)
            
            # Extract the status
            status_element = item.find_element(By.XPATH, './/div[@class="span3 submissions-title"]/p[contains(@class, "small")]')
            status = status_element.text.strip()
            #print('Status:', status)
            
            # Extract the score percentage
            score_percentage = item.find_element(By.XPATH, './/div[@class="span1 submissions-title"][2]/p[@class="small"]').text
            #print('Score Percentage:', score_percentage)
            
            # Extract the 'Yes/No' status
            yes_no_status = item.find_element(By.XPATH, './/div[@class="span1 submissions-title"][4]/p[@class="small"]').text
            #print('Yes/No Status:', yes_no_status)
            
            # Extract the 'View' link
            view_link = item.find_element(By.XPATH, './/div[@class="span1"]/p[@class="btn-wrap"]/a').get_attribute('href')
            #print('View Link:', view_link)

            if yes_no_status == "Yes":
              submission = Submissions.objects.create(problemName = str(problem_name),username = str(username),submissionId = int(submission_id),lang = str(language),srcLink = str(view_link))
              if submission:
                print("Row inserted successfully")
              
            
            print('---')
      page += 1


#hacker = HackerRankSession(username,password)


#print(hacker.fetch_code("https://www.hackerrank.com/contests/scavenger-hunt-7/challenges/can-place-flowers-1/submissions/code/1358824545"))

#hacker.fetch_data("contests/scavenger-hunt-7/judge/submissions")


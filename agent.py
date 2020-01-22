from database import Database
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import json

class Agent():

    def __init__(self):
        options = Options()
        #options.headless = True
        self.driver = webdriver.Chrome(executable_path = "./chromedriver", options=options)
        self.d = Database()

    def handle_urls(self):
        urls = []
        with open('courses.json') as json_file:
            urls = json.load(json_file)
        self.duo_authentication() 

        #hacky way to handle wierd exceptions
        #atlas.ai serves timeouts at every 1000-2000 requests. Not sure which number
        #From the same IP. Easy to maneauver but too lazy to code it in. Can do this manually as 
        #number of times i really need to run the program will be round 6 times. Not worth coding logic in
        number = 10677
        print(len(urls))
        while(number < len(urls)):
            self.scrape_course_page(urls[number])
            number = number+1

        #original way
        #for url in urls:
        #   self.scrape_course_page(url)
                

    def scrape_course_page(self,url):
        self.driver.get(url)
        WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,"legal-container")))

        #according to database scheme, scrape and append to dataentry
        data_entry = [] 

        #CourseID
        elem = self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div/h2") 
        if len(elem)>0: 
            print("CourseID " + elem[0].text.strip())
            data_entry.append(elem[0].text.strip())
        else:
            data_entry.append("")
        
        #Coursename
        elem =self.driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div[1]/h1") 
        if len(elem)>0:
            print("CourseName " + elem[0].text)
            data_entry.append(elem[0].text)
        else:
            data_entry.append("")

        #Median
        elem = self.driver.find_elements_by_xpath( "/html/body/div[1]/div[1]/div/div[2]/div/p[1]/span")
        if len(elem)>0:
            e = elem[0]
            print("Course Median " + e.text.strip())
            data_entry.append(e.text.strip())
        else:
            data_entry.append("")

        #Workload
        elem = self.driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[3]/div[1]/h5")
        if len(elem)>0: 
            elem =self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[3]/div[1]/h5")
            text = elem.text
            temp = list(text)
            temp[-1] = ""
            print("Workload "+ ''.join(temp))
            data_entry.append(''.join(temp))
        else: 
            data_entry.append(-1)

        #Should update column with credits
        #Should update column with department

        self.d.create_entry(data_entry)

    #code to bypass duo authentication. Challenging as they started using pseudoselectors 
    #to prevent phantom touches. However, easy to bypass (chrome shortcuts)
    def duo_authentication(self):

        #login credentials are safe in login.txt 
        #login.txt included in gitignore
        self.driver.get("https://duo.it.umich.edu/")
        username = ""
        passwd = ""
        with open("login.txt",'r') as login_file:
            username = login_file.readline()
            passwd = login_file.readline()
        b = base64.b64decode((passwd))
        passwd = b.decode("utf-8")

        WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"login")))
        login = self.driver.find_element_by_id("login")
        login.clear()
        login.send_keys(username)

        WebDriverWait(self.driver,100).until(EC.presence_of_element_located((By.ID,"password")))
        password = self.driver.find_element_by_id("password")
        password.send_keys(passwd)
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        
        time.sleep(7)
        self.driver.refresh()
        time.sleep(3)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(10)
    
    #used to generate all the url links
    #outputs links to courses.json
    def scrape_course_links(self):

        self.driver.get("https://www.atlas.ai.umich.edu")
        search = self.driver.find_element_by_xpath("""//*[@id="search"]""")
        search.send_keys("a")
        search.send_keys(Keys.ENTER)
        print("Success. Souping up the data")
        time.sleep(5)
        links = []
        results = self.driver.find_elements_by_class_name("course1")

        with open("courses.json",'w') as json_file:
            for link in results:
                link = link.find_element_by_tag_name("a").get_attribute("href")
                links.append(link)
            json.dump(links,json_file)

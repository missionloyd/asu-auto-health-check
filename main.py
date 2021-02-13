# created by an ASU student, "missionloyd"
# give this project a lil star on GitHub if you're looking at the source code :)
# pipreqs

import time, json, sys
from getpass import getpass
from os.path import exists
from selenium import webdriver
from cryptography.fernet import Fernet

creds = "\n\n*** Created by Missionloyd :) ***\nhttps://github.com/missionloyd\n"

print("\n*** Hello, this is your automatic health checker ***\n\nFor issues/errors, please go to this link:\nhttps://github.com/missionloyd/asu-auto-health-check/issues\n")
time.sleep(1)

#credentials to My ASU
credential = {
    "username": None,
    "password": None
}

#ask user for credentials
def get_credential():
    print("Please fill in your My ASU credentials\n(Your info will encrypted, saved locally and will NOT be shared to ANYONE)\n")
    username = input("Username: ")
    password = getpass()
    print("\n")
    return username, password

#encrypt username and password
if not exists("cred.enc"):

    #generate keys 
    key = Fernet.generate_key()
    cipher = Fernet(key)

    #load credentials encode/encrypt
    credential['username'], credential['password'] = get_credential()
    credential_byte = json.dumps(credential).encode('utf-8')
    cred_enc = cipher.encrypt(credential_byte)

    #save encoded credentials to a file and save key to seperate file
    with open("cred.enc", "wb") as f1, open("cred.key", "wb") as f2:
        f1.write(cred_enc)
        f2.write(key)

#decrypt, open encoded credentials and open key
with open("cred.enc", "rb") as f1, open("cred.key", "rb") as f2:
    cred_decrypt = f1.read()
    key = f2.read()
    cipher = Fernet(key)
    data = json.loads(cipher.decrypt(cred_decrypt).decode('utf-8'))

#set username and password
username = data["username"]
password = data["password"]

#asu login element paths
username_input = '//*[@id="username"]'
password_input = '//*[@id="password"]'
login_submit = '/html/body/div/div/main/div/div/div/div/form/section[2]/div[1]/input'

#health check element paths
health_form_open = '/html/body/header/div[2]/div/div/div/nav/div/div[2]/form/div/a'
health_form_already_done = '/html/body/div/div/main/div/div/div[2]/button'
q1_none = '/html/body/div/div/main/div/div/div[3]/div/div[2]/button[4]'
q1_next = '/html/body/div/div/main/div/div/div[3]/div/div[3]/button'
q2_none = '/html/body/div/div/main/div/div/div[3]/div/div[3]/button'
submit = '/html/body/div/div/main/div/div/div[3]/div/div[4]/button'


#for finding the frame of the form
def switch_to_iFrame():
    frame = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/iframe')
    driver.switch_to.frame(frame)

#######################

#open firefox and login
#https://chromedriver.chromium.org/downloads
try:
    print("Openeing Firefox and logging in...\n")

    # If chrome driver is installed in this folder
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--enable-javascript")
    # driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')

    driver = webdriver.Firefox()

    driver.get('https://www.asu.edu/healthcheck/preferences.html#')
    time.sleep(1.5)
except:
    print("\nError... Looks Like you do not have FireFox installed!\nOr the URL to the form has changed!")
    sys.exit()

#send keys and sumbit login
try:
    driver.find_element_by_xpath(username_input).send_keys(username)
    print("*\n")
    driver.find_element_by_xpath(password_input).send_keys(password)
    print("*\n")
    driver.find_element_by_xpath(login_submit).click()
except:
    print("\nError... Looks like we had trouble logging in...\n\nYour login info may not be correct...\n* Delete both \"cred\" files to reset credentials *")
    driver.close()
    sys.exit()

#update user
print("Now filling out the health check form...\n")
time.sleep(1)

#find health form
try:
    driver.find_element_by_xpath(health_form_open).click()
    print("*\n")
    time.sleep(2)
    #switch to iFrame
    switch_to_iFrame()
except:
    print("Error... Could not locate health form!\n\nYour login info may not be correct...\n* Delete both \"cred\" files to reset credentials *")
    driver.close()
    sys.exit()

#kill process if the form is already filled out

try:
    driver.find_element_by_xpath(health_form_already_done)
except:

#Q1 "Are you experiencing new or worsening of any of the following?"
    driver.find_element_by_xpath(q1_none).click()
    print("*\n")
    time.sleep(0.5)

    #Q1 next
    driver.find_element_by_xpath(q1_next).click()
    print("*\n")
    time.sleep(1.5)

    #Q2 
    driver.find_element_by_xpath(q2_none).click()
    print("*\n")
    time.sleep(0.5)

    #done
    driver.find_element_by_xpath(submit).click()
    print("*\n")
    time.sleep(0.5)

    print("Done! Now closing your browser...")
    print(creds)
    time.sleep(1)
    driver.close()
    sys.exit()

print("You already filled out your health form today...")
print(creds)
driver.close()
sys.exit()
# created by an ASU student, "missionloyd"
# give this project a lil star on GitHub if you're looking at the source code :)

import time, json, sys
from selenium import webdriver

creds = "\n\n*** Created by Missionloyd :) ***\nhttps://github.com/missionloyd\n"

print("\n*** Hello, this is your automatic health checker ***\n\nFor issues/errors, please go to this link:\nhttps://github.com/missionloyd\n")
time.sleep(1)

#open config file for credentials
with open("config.json","r+") as f:
    config = json.load(f)

    #first time login
    if (config["username"] == "" or config["password"] == ""):
            print("Please fill in your My ASU credentials\n(Your info will be saved locally and will NOT be shared to ANYONE)\n")
            config["username"] = input("Username: ")
            config["password"] = input("Password: ")
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()

    username = str(config["username"])
    password = str(config["password"])

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
try:
    print("Openeing Firefox and logging in...\n")
    driver = webdriver.Firefox()
    driver.get('https://www.asu.edu/healthcheck/preferences.html')
    time.sleep(3)
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
    print("\nError... Looks like we had trouble logging in...\n\nCheck your login info in the config file!")
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
    print("Error... Could not locate health form!\n\n(Maybe check your login info in the config file!)")
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
    time.sleep(0.5)

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
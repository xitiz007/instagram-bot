from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


class Instagram:
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
        self.driver = webdriver.Chrome()
        self.baseurl = 'https://www.instagram.com/'

    def login(self):
        try:
            self.driver.get(f'{self.baseurl}accounts/login')
            time.sleep(2)
            self.driver.find_element_by_name('username').send_keys(self.phone)
            self.driver.find_element_by_name('password').send_keys(self.password)
            self.driver.find_element_by_name('password').send_keys(Keys.ENTER)
            time.sleep(3)
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
            time.sleep(1)
            self.profile_link = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').get_attribute('href')
            time.sleep(1)
        except Exception:
            print('Something went wrong')

    def searchuser(self, username):
        self.driver.get(f'{self.baseurl}{username}/')
        time.sleep(2)

    def followuser(self, username):
        self.searchuser(username)
        try:
            text = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/div[1]/button').text
            if text == 'Follow':
                self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[1]/button').click()
            else:
                print(f'You have requested {username} to follow')
        except Exception:
            text = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').text
            if text == 'Follow':
                self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
            else:
                print('you have already followed ', username)

    def followusers(self, usernames):
        for username in usernames:
            self.followuser(username)
            time.sleep(2)

    def unfollowuser(self, username):
        time.sleep(1)
        self.searchuser(username)
        try:
            text = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').text
        except Exception:
            print('Something went wrong or you might have not followed ', username)
        else:
            if text == 'Following':
                self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
                time.sleep(1)
                print('Successfully unfollowed ', username)
            else:
                print('You are not following {} so you can\'t unfollow'.format(username))

    def unfollowusers(self, usernames):
        for username in usernames:
            self.unfollowuser(username)
            time.sleep(2)

    def profile(self):
        self.driver.get(self.profile_link)
        time.sleep(2)

    def setting(self):
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button/span').click()
        time.sleep(2)

    def logout(self):
        self.profile()
        self.setting()
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()
        time.sleep(1)

    def editprofile(self):
        self.profile()
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/a/button').click()
        time.sleep(2)

    def setname(self, name):
        if self.checkbioandname(name):
            self.editprofile()
            self.driver.find_element_by_xpath('//*[@id="pepName"]').clear()
            self.driver.find_element_by_xpath('//*[@id="pepName"]').send_keys(name)
            self.submit()
        else:
            print('Wrong argument passed')

    def setbio(self, bio):
        if self.checkbioandname(bio):
            self.editprofile()
            self.driver.find_element_by_xpath('//*[@id="pepBio"]').clear()
            self.driver.find_element_by_xpath('//*[@id="pepBio"]').send_keys(bio)
            self.submit()
        else:
            print('Wrong argument passed')

    def submit(self):
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/form/div[10]/div/div/button[1]').click()
        time.sleep(1)
        self.profile()

    def changepassword(self, current_password, new_password):
        current_password = current_password.strip()
        new_password = new_password.strip()
        if current_password == '' or new_password == '':
            print('Incorrect password entry')
        else:
            self.editprofile()
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/ul/li[2]/a').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="cppOldPassword"]').send_keys(current_password)
            self.driver.find_element_by_xpath('//*[@id="cppNewPassword"]').send_keys(new_password)
            self.driver.find_element_by_xpath('//*[@id="cppConfirmPassword"]').send_keys(new_password)
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/article/form/div[4]/div/div/button').click()

    def checkbioandname(self, text):
        return not text.strip() == ''

    def checkusernames(self, usernames):
        return len(usernames) != 0

    def showrecentpost(self):
        try:
            link = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a').get_attribute(
                'href')
            self.driver.get(link)
            time.sleep(2)
        except Exception:
            print('Something went wrong')

    def likeonpost(self):
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button').click()
            time.sleep(2)
        except Exception:
            print('Something went wrong')

    def likeonrecentpost(self, username):
        time.sleep(1)
        self.searchuser(username)
        self.showrecentpost()
        self.likeonpost()
        time.sleep(2)


phone_number = os.environ.get('phone_number')
password = os.environ.get('password')

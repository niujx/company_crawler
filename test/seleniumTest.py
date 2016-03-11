# -*- coding: utf-8 -*-
from selenium import webdriver
import threading
import time

browser = webdriver.Firefox()
browser.get('http://36kr.com/')
browser.find_element_by_link_text('登录/注册').click()
browser.find_element_by_name('username').send_keys('qianglin@k2vc.com')
browser.find_element_by_name('password').send_keys('0322zhang')
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/button').click()

time.sleep(90)
print 'start cookie'
print browser.get_cookies()

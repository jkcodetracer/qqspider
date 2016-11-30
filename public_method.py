#!/usr/bin/python
# encoding=utf-8

import requests
import time
import json
import random 
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from yundama import identify

def get_cookie(account, password, dama=False):
    """ 根据QQ号和密码获取cookie """
    failure = 0
    while failure < 3:
        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
            )
            browser = webdriver.PhantomJS(desired_capabilities=dcap)
            browser.get('http://qzone.qq.com/')
            try:
                access = browser.find_element_by_id('guideSkip')  # 继续访问触屏版按钮
                access.click()
                time.sleep(1)
            except Exception, e:
                pass

            account_input = browser.find_element_by_id('u')  # 账号输入框
            password_input = browser.find_element_by_id('p')  # 密码输入框
            go = browser.find_element_by_id('go')  # 登录按钮
            account_input.clear()
            password_input.clear()
            account_input.send_keys(account)
            password_input.send_keys(password)
            go.click()
            time.sleep(2)

            while '验证码' in browser.page_source:
                try:
                    print '需要处理验证码！'
                    browser.save_screenshot('verification.png')
                    if not dama:  # 如果不需要打码，则跳出循环
                        break
                    iframes = browser.find_elements_by_tag_name('iframe')
                    try:
                        browser.switch_to_frame(iframes[1])
                        input_verification_code = browser.find_element_by_id('cap_input')
                        submit = browser.find_element_by_id('verify_btn')
                        verification_code = identify()
                        print '验证码识别结果: %s' % verification_code
                        input_verification_code.clear()
                        input_verification_code.send_keys(verification_code)
                        submit.click()
                        time.sleep(1)
                    except Exception, e:
                        break
                except Exception, e:
                    browser.quit()
                    return ''
            if browser.title == 'QQ空间':
                cookie = {}
	        print "get cookie!"
                for elem in browser.get_cookies():
                    cookie[elem['name']] = elem['value']
                print 'Get the cookie of QQ:%s successfully!(共%d个键值对)' % (account, len(cookie))
                browser.quit()
                return json.dumps(cookie)  # 将字典转成字符串
            else:
                print 'Get the cookie of QQ:%s failed!' % account
                return ''
        except Exception, e:
            failure = failure + 1
            if 'browser' in dir():
                browser.quit()
        except KeyboardInterrupt, e:
            raise e
    return ''


get_cookie("365027110", "ella198809100617")



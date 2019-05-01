#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
info:
author:uasier
github:https://github.com/hfut2016/
update_time:2019-4-1
"""

import time  # 用来延时
from selenium import webdriver  # selenium方式爬数据
import pymysql  # 用来操作数据库
import logging  # 设置日志

def single(num):   # 单选题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/1")
    time.sleep(5)  # 等待
    for index in range(1, 51):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            option1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[2]/span[2]").text
            option2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[2]/span[2]").text
            option3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[2]/span[2]").text
            option4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[2]/span[2]").text
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            answer2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[1]").get_attribute('class')
            answer3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[1]").get_attribute('class')
            answer4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[1]").get_attribute('class')
            answer = ''
            if answer1 == "ivu-radio ivu-radio-checked":
                answer = 'A'
            if answer2 == "ivu-radio ivu-radio-checked":
                answer = 'B'
            if answer3 == "ivu-radio ivu-radio-checked":
                answer = 'C'
            if answer4 == "ivu-radio ivu-radio-checked":
                answer = 'D'
            add_data(question, answer, option1, option2, option3, option4)

def multiple(num):   # 多选题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/2")
    time.sleep(5)  # 等待
    for index in range(1, 21):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            option1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[2]/span[2]").text
            option2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[2]/span[2]").text
            option3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[2]/span[2]").text
            option4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[2]/span[2]").text
            option5 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[5]/span[2]/span[2]").text
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            answer2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[1]").get_attribute('class')
            answer3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[1]").get_attribute('class')
            answer4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[1]").get_attribute('class')
            answer5 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[5]/span[1]").get_attribute('class')
            answer = ''
            if answer1 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'A'
            if answer2 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'B'
            if answer3 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'C'
            if answer4 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'D'
            if answer5 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'E'
            print(answer)
            add_data(question, answer, option1, option2, option3, option4, option5)

def judge(num):   # 判断题处理
    # driver.get("https://exam.scctedu.com/#/130426")
    # time.sleep(5)  # 等待
    el = driver.find_elements_by_xpath('//*[@id="container"]/form/div[3]/div/div/div[1]/div')
    for index in range(1, len(el)+1):
        try:
            '''
            '''
            question = driver.find_element_by_xpath('//*[@id="container"]/form/div[3]/div/div/div[1]/div[%s]/div/div/div[2]/span' %index).text
            if (question):
                print(question)
                answer1 = driver.find_element_by_xpath('//*[@id="container"]/form/div[3]/div/div/div[1]/div[%s]/div[2]/div/label[1]' %index)
                answer2 = driver.find_element_by_xpath('//*[@id="container"]/form/div[3]/div/div/div[1]/div[%s]/div[2]/div/label[2]' %index)
                # print(answer1.text)
                if index>10 == 0:
                    answer1.click()
                else:
                    answer2.click()
            else:
                answer1 = driver.find_element_by_xpath('//*[@id="container"]/form/div[3]/div/div/div[1]/div[1]/div[2]/div/label[1]')
                if answer1 == "ivu-radio ivu-radio-checked":
                    answer = '对'
                else:
                    answer = '错'
                # print(question, answer)
        except Exception as err:
            print('====>',err)

def login(user):    # 登录系统
    # tel = input('请输入你的账号：')
    # pwd = input('请输入你的密码：')
    driver.get("https://user.scctedu.com/login")

    driver.find_element_by_id('doc-vld-name-2-1').clear()
    driver.find_element_by_id('doc-vld-name-2-1').send_keys(user['stuid'])  # 此处输入账号
    driver.find_element_by_id('doc-vld-pwd-1-0').clear()
    driver.find_element_by_id('doc-vld-pwd-1-0').send_keys(user['pwd'])  # 此处输入密码
    driver.find_element_by_id('login-button').click()
    time.sleep(5)  # 等待

if __name__ == '__main__':  # 测试主函数
    option = webdriver.ChromeOptions()
    option.add_argument('cookie=Hm_lvt_b5cebd5cc0bb0563baad44cac9ee9594=1555115135,1555157629,1555337415,1555495037; XSRF-TOKEN=eyJpdiI6IjZVeDVkZXp4Y2I4dEdabHZDYzRJZ1E9PSIsInZhbHVlIjoiMk5TbnJJdzdsS1V0N1YyRlVEVStrWDdVVjRya3NzS2VLS0Vaa1RCaEpZXC9IcjNPRURxWmRYZTVxbGRvOHhHQWQiLCJtYWMiOiI4OWZhNTQ2YjZhMTBjMGY1NzFlOWUzNmZmNTZlNzEzOWI2NzgzZjU4M2M0NTM0NWRmNmJhN2I2MDZlMWI4MTBlIn0%3D; scctedu_session=eyJpdiI6ImJmSm03V0F0Q0VCc1NhS3QwMmdLeHc9PSIsInZhbHVlIjoiTFFUU1wvVG5sSE92eWl0dE1tR3VyVzFnVVNGSVhya0Y5VlQxTURqdDU1TnJCU3dRMXRnSFpWUXRybWUyZXNFa2EiLCJtYWMiOiJlMWI3N2I5YjUyOGEzYTI3NjA2YWE2MjdmMzA4YWViYzgyY2UxMjZhZWI5MjNlMWY1N2VkYWJjNjgyNjYxMDE0In0%3D; local_expired_at=1555584002; local_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zY2N0ZWR1LmNvbS9hcGkvYXV0aG9yaXphdGlvbnMvY3VycmVudCIsImlhdCI6MTU1NTQ5NTA0NywiZXhwIjoxNTU1NTk4Mzg5LCJuYmYiOjE1NTU1ODM5ODksImp0aSI6InJBM0EyNVB4cExLcXA1WU0iLCJzdWIiOjIyNjcxLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.10w2PMjmLw6oatUdZ079LlreXSkFTaHzLGB76Iaq1YE; CONTAINERID=28915df92f2ca9281f4ad90700f9ca61b95ba3e0e071f76719c6faf09645545a|XLhXq|XLhT+; Hm_lpvt_b5cebd5cc0bb0563baad44cac9ee9594=1555585007')
    option.add_argument('if-modified-since=Wed, 20 Mar 2019 05:49:00 GMT')
    option.add_argument('if-none-match= "5c91d44c-2a9"')
    option.add_argument('upgrade-insecure-requests= 1')
    option.add_argument('Origin= https://exam.scctedu.com')
    option.add_argument('Referer= https://exam.scctedu.com/')
    driver = webdriver.Chrome('E:\wamp\Demo\chromedriver.exe',chrome_options=option)  # 选择浏览器，此处我选择的Chrome
    # login(user=user)
    try:
        # mysql_connect_init()  # 初始化数据库
        # create_table()  # 数据库
        ran = 266902
        # while ran < 267100:
        get_token = 'eyJpc3MiOiJodHRwczovL2FwaS5zY2N0ZWR1LmNvbS9hcGkvYXV0aG9yaXphdGlvbnMvY3VycmVudCIsImlhdCI6MTU1NTQ5NTA0NywiZXhwIjoxNTU1NTk4Mzg5LCJuYmYiOjE1NTU1ODM5ODksImp0aSI6InJBM0EyNVB4cExLcXA1WU0iLCJzdWIiOjIyNjcxLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0'
        driver.execute_script('localStorage.setItem("Token", %s);'% get_token)
        driver.get('wss://message.scctedu.com:11300/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zY2N0ZWR1LmNvbS9hcGkvYXV0aG9yaXphdGlvbnMvY3VycmVudCIsImlhdCI6MTU1NTQ5NTA0NywiZXhwIjoxNTU1NTk4Mzg5LCJuYmYiOjE1NTU1ODM5ODksImp0aSI6InJBM0EyNVB4cExLcXA1WU0iLCJzdWIiOjIyNjcxLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.10w2PMjmLw6oatUdZ079LlreXSkFTaHzLGB76Iaq1YE')
        driver.get("https://exam.scctedu.com/#/home")  # 用来强制更新页面
        driver.get("https://exam.scctedu.com/#/130426")
        while True:
            # noinspection PyBroadException
            try:
                # single(str(ran))
                # multiple(str(ran))
                judge(str(ran))
            except Exception as err:    # 捕捉任何异常，保证程序可以继续运行下去
                # logger.critical(str(ran) + " : " + str(err))
                print(str(ran) + " : " + str(err))
                # 如果出问题了，那就直接跳过这个
            finally:
                ran = ran + 1
    except Exception as err:
        print("程序执行出错：", err)
    else:
        print("程序执行成功")
    finally:
        print("main执行完毕")

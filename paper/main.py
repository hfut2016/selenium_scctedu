#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
info:
author:uasier
github:https://github.com/uasier/
update_time:2019-4-1
"""

import time  # 用来延时
from selenium import webdriver  # selenium方式爬数据
import pymysql,xlwt  # 用来操作数据库
import logging  # 设置日志
from paper import setting,mysqlCreat

# 日志相关配置
logger = logging.Logger('log', level=logging.WARNING)
sh = logging.StreamHandler()
fh = logging.FileHandler('log.log', encoding='utf-8')
fmt = logging.Formatter('%(threadName)s %(levelname)s %(lineno)s行: - %(asctime)s\n\t %(message)s', '%d %H:%M')
sh.setFormatter(fmt)
fh.setFormatter(fmt)
logger.addHandler(sh)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


def login(user):  # 登录系统
    # tel = input('请输入你的账号：')
    # pwd = input('请输入你的密码：')
    driver.get("https://user.scctedu.com/login")

    driver.find_element_by_id('doc-vld-name-2-1').clear()
    driver.find_element_by_id('doc-vld-name-2-1').send_keys(user['stuid'])  # 此处输入账号
    driver.find_element_by_id('doc-vld-pwd-1-0').clear()
    driver.find_element_by_id('doc-vld-pwd-1-0').send_keys(user['pwd'])  # 此处输入密码
    driver.find_element_by_id('login-button').click()
    time.sleep(5)  # 等待


def single(num):  # 单选题处理
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


def multiple(num):  # 多选题处理
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


def judge(num):  # 判断题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/3")
    time.sleep(5)  # 等待
    for index in range(1, 11):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            if answer1 == "ivu-radio ivu-radio-checked":
                answer = '对'
            else:
                answer = '错'
            add_data(question, answer)


def findTitle(num):
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/1  ")
    time.sleep(5)  # 等待
    title = driver.find_element_by_xpath(
        '//*[@id="main"]/div[1]/div[1]/div/form/div[1]/div/div/div/div[1]/p/span[1]/span[1]')
    if title:
        option = ['', '', '']
        opel = driver.find_elements_by_xpath('//*[@id="main"]/div[1]/div[1]/div/form/div[1]/div/div/div/div[2]/div/button')
        for item in range(0, len(opel)):
            option[item] = driver.find_element_by_xpath(
                '//*[@id="main"]/div[1]/div[1]/div/form/div[1]/div/div/div/div[2]/div/button[{0}]'.format(str(item+1))).text
        return {'index': num, 'title': title.text, 'option': option}
    else:
        return {'index': num}


def toExcel(data, output_path):
    workbook = xlwt.Workbook()

    # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
    # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
    sheet = workbook.add_sheet('table_', cell_overwrite_ok=True)

    # 获取并写入数据段信息
    row = 0
    col = 0
    for row in range(0, len(data)):
        sheet.write(row, 1, u'%s' % data[row]['title'])
        sheet.write(row, 0, u'%s' % data[row]['index'])

    workbook.save(output_path)


if __name__ == '__main__':  # 测试主函数
    driver = webdriver.Chrome('E:\wamp\Demo\chromedriver.exe')  # 选择浏览器，此处我选择的Chrome
    login(user=setting.USER3)
    try:
        # mysql_connect_init()  # 初始化数据库
        # create_table()  # 数据库
        # ran = 266902
        mysql = mysqlCreat.MYSQL()
        mysql.connect_db(config=setting.DB_CONFIG_2)  #
        mysql.set_table('paper_index')
        add_data = mysql.add_data
        select_data = mysql.select_data

        ran = 333890
        while ran < 348100:
            # noinspection PyBroadException
            try:
                if select_data(question=str(ran)):
                    continue
                else:
                    driver.get("https://exam.scctedu.com/#/home")  # 用来强制更新页面
                    time.sleep(1)
                    el = findTitle(str(ran))
                    if el['title'] == '':
                        print(ran)
                    else:
                        print(el)
                        add_data(question=el['index'], answer=el['title'], option1=el['option'][0], option2=el['option'][1], option3=el['option'][2])
            except Exception as err:    # 捕捉任何异常，保证程序可以继续运行下去
                logger.critical(str(ran) + " : " + str(err))
                print(str(ran) + " : " + str(err))
                # 如果出问题了，那就直接跳过这个
            finally:
                ran = ran + 1
    except Exception as err:
        print("程序执行出错：", err)
    else:
        print("程序执行成功")
    finally:
        # toExcel(data, 'E:/test_input.xls')
        print("main执行完毕")

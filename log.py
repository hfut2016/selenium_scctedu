#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
info:
author:uasier
github:https://github.com/uasier/
update_time:2019-4-1
"""

import time  # 用来延时
from selenium import webdriver  # selenium方式爬数据
import logging  # 设置日志

# 日志相关配置
# logger = logging.Logger('log', level=logging.WARNING)
# sh = logging.StreamHandler()
# fh = logging.FileHandler('log.log', encoding='utf-8')
# fmt = logging.Formatter(' %(asctime)s %(pathname)s  %(lineno)s行: \n\t %(message)s','%Y/%m/%d %H:%M:%S')
# sh.setFormatter(fmt)
# fh.setFormatter(fmt)
# logger.addHandler(sh)
# logger.addHandler(fh)
# logger.setLevel(logging.INFO)

def log(name, logFile='log.log'):
    # 创建Logger
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)

    # 创建Handler

    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 文件Handler
    fileHandler = logging.FileHandler(logFile, mode='w', encoding='UTF-8')
    fileHandler.setLevel(logging.NOTSET)

    # Formatter
    formatter = logging.Formatter('%(asctime)s- %(name)s -%(pathname)s  %(lineno)s行: - %(message)s','%Y/%m/%d %H:%M:%S')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加到Logger中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    return logger

def login(user):  # 登录系统
    # tel = input('请输入你的账号：')
    # pwd = input('请输入你的密码：')
    driver.get("http://172.16.200.13")

    driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[5]/td[2]/input').clear()
    driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[5]/td[2]/input').send_keys(
        user['name'])  # 此处输入账号
    driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[6]/td[2]/input').clear()
    driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[6]/td[2]/input').send_keys(
        user['pwd'])  # 此处输入密码
    driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[7]/td/p/input[1]').click()
    time.sleep(1.5)  # 等待


def check():
    driver.get('https://www.baidu.com/')
    time.sleep(1.5)
    info = {
        'hasLoging': True,
        'message': ''
    }
    try:
        btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr[7]/td/p/input[1]')
    except Exception as err:
        btn = ''
        # print(err)
    finally:
        if btn:
            info['hasLoging'] = False
        return info


check_time = 2

if __name__ == '__main__':  # 测试主函数
    driver = webdriver.Chrome('E:\wamp\Demo\chromedriver.exe')  # 选择浏览器，此处我选择的Chrome
    mylog = log('auto')
    try:
        count_login = 0
        while True:
            try:
                res = check()
                if res['hasLoging']:
                    time.sleep(check_time)
                    continue
                else:
                    login(user=user)  # 用来强制更新页面
                    count_login += 1
            except Exception as err:  # 捕捉任何异常，保证程序可以继续运行下去
                # logger.critical(time.strftime('%m-%d %H:%M') + " : 自动登陆共{0}次".format(count_login) + " \n " + str(err))
                # 如果出问题了，那就直接跳过这个
                mylog.warning(str(err))
                print(err.args)
                if 'chrome not reachable' in err.args[0] or 'no such window' in err.args[0]:
                    driver.quit()
                    driver = webdriver.Chrome('E:\wamp\Demo\chromedriver.exe')
                else:
                    print('****'*6)

            finally:
                print(str(time.strftime('%m-%d %H:%M')) + " : 自动登陆共{0}次".format(count_login))
                mylog.info(" : 自动登陆共{0}次".format(count_login))
    except Exception as err:
        print("程序执行出错：", err)
    else:
        print("程序执行成功")
    finally:
        # toExcel(data, 'E:/test_input.xls')
        print("main执行完毕")

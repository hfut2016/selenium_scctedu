import time  # 用来延时
from selenium import webdriver  # selenium方式爬数据
import xlrd
from paper import mysqlCreat
from paper import setting

def creatCounter():
    s = [0]

    def counter():
        s[0] = s[0] + 1
        return s[0]

    return counter
def single(num):  # 单选题处理
    """
    :param num:
    :return:
    """
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/1")
    # WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
    time.sleep(5)  # 等待
    el = driver.find_elements_by_xpath(
        '//*[@id="main"]/div[1]/div[1]/div/form/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]')
    for index in range(1, len(el) + 1):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            els = driver.find_elements_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                    index) + "]/div[2]/div/div/div/div[2]/div/label")
            option = ['', '', '', '', '', '']
            answer = '%'
            # 选项总数
            for id in range(1, len(els) + 1):
                option[id] = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                    index) + "]/div[2]/div/div/div/div[2]/div/label[" + str(id) + "]/span[2]/span[2]").text
                answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                    index) + "]/div[2]/div/div/div/div[2]/div/label[" + str(id) + "]/span[1]").get_attribute('class')
                if answer1 == "ivu-radio ivu-radio-checked":
                    answer = chr(64 + id)  # chr(ord('A') - 1 + id)

            add_data(question, answer, option[1], option[2], option[3], option[4])
    questiontype = driver.find_elements_by_xpath(
        '//*[@id="main"]/div[1]/div[1]/div/form/div[1]/div/div/div/div[2]/div/button')
    for item in range(2, len(questiontype)+1):
        option = driver.find_element_by_xpath(
            '//*[@id="main"]/div[1]/div[1]/div/form/div[1]/div/div/div/div[2]/div/button[{0}]'.format(
                str(item))).text
        if '多' in option:
            multiple(num)  # 多选题
        elif '判' in option:
            judge(num)  # 判断题



def judge(num):  # 判断题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/3")
    time.sleep(1.5)  # 等待
    el = driver.find_elements_by_xpath(
        '//*[@id="main"]/div[1]/div[1]/div/form/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]')
    for index in range(1, len(el)):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            if answer1 == "ivu-radio ivu-radio-checked":
                answer = '正确'
            else:
                answer = '错误'
            add_data(question, answer)


def multiple(num):  # 多选题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/2")
    time.sleep(1.5)  # 等待
    el = driver.find_elements_by_xpath(
        '//*[@id="main"]/div[1]/div[1]/div/form/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]')
    # 题目总数
    for index in range(1, len(el) + 1):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            els = driver.find_elements_by_xpath('//*[@class="paper-inner"]/div/div[1]/div[' + str(
                index) + ']/div[2]/div/div/div/div[2]/div[2]/label')
            option = ['0', '1', '2', '3', '4', '5','6']
            answer = ''
            # 选项总数
            for id in range(1, len(els) + 1):
                option[id] = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                    index) + "]/div[2]/div/div/div/div[2]/div/label[" + str(id) + "]/span[2]/span[2]").text
                answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                    index) + "]/div[2]/div/div/div/div[2]/div/label[" + str(id) + "]/span[1]").get_attribute('class')
                if answer1 == "ivu-checkbox ivu-checkbox-checked":
                    answer += chr(64 + id)  # chr(ord('A') - 1 + id)

            add_data(question, answer, option[1], option[2], option[3], option[4], option[5])


def login(user):  # 登录系统
    driver.get("https://user.scctedu.com/login")

    driver.find_element_by_id('doc-vld-name-2-1').clear()
    driver.find_element_by_id('doc-vld-name-2-1').send_keys(user['stuid'])  # 此处输入账号
    driver.find_element_by_id('doc-vld-pwd-1-0').clear()
    driver.find_element_by_id('doc-vld-pwd-1-0').send_keys(user['pwd'])  # 此处输入密码
    driver.find_element_by_id('login-button').click()
    time.sleep(5)  # 等待


def paper(sheet):
    global counter
    counter = creatCounter()
    for index in sheet.col_values(0):
        # noinspection PyBroadException
        index = int(index)
        try:
            driver.get("https://exam.scctedu.com/#/home")  # 用来强制更新页面
            time.sleep(0.8)
            single(str(index))
        except Exception as err:  # 捕捉任何异常，保证程序可以继续运行下去
            print(str(index) + " : " + str(err))
            # 如果出问题了，那就直接跳过这个
        finally:
            print(str(index) + " : 执行完毕!")


if __name__ == '__main__':  # 测试主函数
    driver = webdriver.Chrome(setting.DRIVE_PATH)  # 选择浏览器，此处我选择的Chrome
    # login(user=setting.USER)
    global add_data, select_data
    workbook = xlrd.open_workbook(setting.PAPER_PATH)
    sheet = workbook.sheet_by_index(2)
    # print(sheet.name, sheet.cell(0, 1).value)

    try:
        mysql = mysqlCreat.MYSQL()
        mysql.connect_db(config=setting.DB_CONFIG_2)  # 初始化数据库
        add_data = mysql.add_data
        select_data = mysql.select_data
        for index in range(0, len(workbook._sheet_list)):
            sheet = workbook.sheet_by_index(index)
            print(sheet.name, sheet.cell(0, 1).value)
            mysql.create_table(table_name=sheet.name, comment=sheet.cell(0, 1).value)  # 建立数据表
            paper(sheet=sheet)
        # add_data = mysql.add_data
        # select_data = mysql.select_data
        # mysql.show_table()

        # for ran in sheet.col_values(0):
        #     # noinspection PyBroadException
        #     try:
        #         driver.get("https://exam.scctedu.com/#/home")  # 用来强制更新页面
        #         ran = int(ran)
        #         single(str(ran))  # 单选题
        #         multiple(str(ran))  # 多选题
        #         # judge(str(ran))       # 判断题
        #     except Exception as err:  # 捕捉任何异常，保证程序可以继续运行下去
        #         # logger.critical(str(ran) + " : " + str(err))
        #         print(str(ran) + " : " + str(err))
        #         # 如果出问题了，那就直接跳过这个
        #     finally:
        #         print(str(ran) + " : 执行完毕!")
    except Exception as err:
        print("程序执行出错：", err)
    else:
        print("程序执行成功")
    finally:
        print("main执行完毕")

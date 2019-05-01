import xlrd, re, pyperclip, time, os, json, pymysql
from paper import setting


def findAnswer(filePath):
    workbook = xlrd.open_workbook(filePath)
    sheetOne = workbook.sheet_by_index(0)
    questionRow = sheetOne.col_values(0)
    answerRow = sheetOne.col_values(1)
    prePaste = ''
    while True:
        nowPaste = pyperclip.paste()
        time.sleep(0.6)
        if nowPaste != prePaste:
            flag = True
            try:
                searchRe = re.compile(nowPaste)
            except:
                searchRe = re.compile('===')
                print('错误:请勿尝试跨行复制')
            print('复制内容', nowPaste, '\n')
            prePaste = nowPaste
            for row in range(sheetOne.nrows):
                if searchRe.findall(questionRow[row]):
                    print('问题=>', questionRow[row], '\n')
                    # 获取答案个数
                    for num in range(len(answerRow[row])):
                        index = ord(answerRow[row][num]) - ord('?') \
                            if ord(answerRow[row][num]) - ord('?') < sheetOne.ncols else 2
                        print('答案' + str(num + 1) + '=>', answerRow[row][num], sheetOne.row(row)[index].value)
                    flag = False
                    break
            flag and print('未找到任何答案')
            print('\n\n')


def openExcel():
    # filePath = './qa.xlsx'
    for root, dirs, files in os.walk(os.getcwd()):
        for fileName in files:
            fileDir, fileType = os.path.splitext(os.path.join(os.getcwd(), fileName))
            if fileType == '.xlsx' or fileType == '.xls':
                filePath = fileDir + fileType
                workbook = xlrd.open_workbook(filePath)
                if workbook.sheet_by_index(0).ncols > 2:
                    return workbook
    return []


def query(workbook, keyWord):
    sheetOne = workbook.sheet_by_index(0)
    questionRow = sheetOne.col_values(0)
    answerRow = sheetOne.col_values(1)
    respone = {
        "kw": keyWord,
        "question": "未找到任何答案",
        "answer": []
    }
    try:
        searchRe = re.compile(keyWord)
    except:
        searchRe = re.compile('===')
        print('错误:请勿尝试跨行复制')

    for row in range(sheetOne.nrows):
        if searchRe.findall(questionRow[row]):
            # print('问题=>',questionRow[row],'\n')
            respone['question'] = questionRow[row]
            # 获取答案个数
            for num in range(len(answerRow[row])):
                index = ord(answerRow[row][num]) - ord('?') \
                    if ord(answerRow[row][num]) - ord('?') < sheetOne.ncols else 2
                # print('答案'+str(num+1)+'=>',answerRow[row][num],sheetOne.row(row)[index].value)
                respone['answer'].append({"option": answerRow[row][num], "value": sheetOne.row(row)[index].value})
            break

    # print('未找到任何答案')
    # print('\n\n')
    return respone


def excel_to_json():
    workbook = openExcel()
    sheetOne = workbook.sheet_by_index(0)
    questionRow = sheetOne.col_values(0)
    answerRow = sheetOne.col_values(1)
    respone = {
        "question": "未找到任何答案",
        "answer": []
    }
    data = []
    print("开始导出数据")
    # 写上字段信息
    try:
        f = open(setting.BASE_PATH + 'data.json', mode='w+')
        for row in range(1, sheetOne.nrows):
            print('\n')
            print('问题=>', questionRow[row])
            respone['question'] = questionRow[row]
            # 获取答案个数
            answer = []
            for num in range(len(answerRow[row])):
                index = ord(answerRow[row][num]) - ord('?') \
                    if ord(answerRow[row][num]) - ord('?') < sheetOne.ncols else 1
                print('答案' + str(num + 1) + '=>', answerRow[row][num], sheetOne.row(row)[index].value)
                answer.append({"option": answerRow[row][num], "value": sheetOne.row(row)[index].value})
            data.append({"question": questionRow[row], "answer": answer})
        f.write(json.dumps(data))
        f.close()
    except Exception as err:
        print('导出错误：', err)
    finally:
        print("数据导出完毕")


def creatCounter():
    s = [0]

    def counter():
        s[0] = s[0] + 1
        return s[0]

    return counter


def test(num):
    if num > 3:
        global coun
        coun = creatCounter()
    else:
        print('-----')


def changeArgs(funNume):
    """
    mysql插入数据参数引号处理
    :param funNume:
    :return:
    """

    def func_in(*args, **kargs):
        newArgs = []
        for arg in args:
            newArgs.append(pymysql.escape_string(arg))
        return funNume(*newArgs, **kargs)

    return func_in


# @changeArgs
def strtest(a, b, c, d):
    print(a, '\n', b, '\n', c, '\n', d)


# print(sheetOne.col(1))
# print(chr(ord('A')-2))
# print(pyperclip.paste())

if __name__ == '__main__':
    # workbook = openExcel()
    # findAnswer(filePath)
    # query(workbook=workbook)
    # excel_to_json()
    a = '1234'
    b = 'sads'
    c = """sldk"""
    d = """sad's"a"l'k"""
    strtest(a, b, c, d)

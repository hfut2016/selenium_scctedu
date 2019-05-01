# __Desc__ = 从数据库中导出数据到excel数据表中
import xlwt, json
import pymysql
from paper import setting
from search import openExcel


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


class MYSQL:
    def __init__(self):
        pass

    def __del__(self):
        try:
            self._cursor.close()
            self._connect.close()
        except Exception as error:
            print("数据库关闭失败：", error)
        else:
            print("数据库关闭成功")
        finally:
            print("close_mysqlDB()函数执行完毕")

    def connect_db(self, config):
        """
        连接数据库
        :return:
        """
        print("开始连接数据库")
        try:
            self._connect = pymysql.Connect(
                host=config['host'],
                user=config['user'],
                passwd=config['passwd'],
                db=config['db'],
                port=3306,
                charset='utf8'
            )
            self._cursor = self._connect.cursor()

        except Exception as error:
            print("数据库打开失败：", error)
        else:
            print("数据库打开成功")
        finally:
            print("setup_mysqlDB()函数执行完毕")

    def show_table(self):
        """
        获取数据库表注释说明
        :return:
        """
        sql = """SELECT
                table_name 表名,
                table_comment 表说明
                FROM
                information_schema.TABLES
                WHERE
                table_schema = 'xszc'
                ORDER BY
                table_name"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def set_table(self, table_name):
        try:
            self._tableName = table_name
        except Exception as error:
            print("set_table失败：", error)
        else:
            print("set_table成功")
        finally:
            print("set_table函数执行完毕")

    def create_table(self, table_name='test', comment='无说明'):  # 创建数据表
        self._tableName = table_name
        print("create_table()函数开始执行")
        try:
            # 使用 execute() 方法执行 SQL，如果表存在则删除
            self._cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
            # 使用预处理语句创建表
            sql = """CREATE TABLE  %s(
                      id  int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                      question varchar(200) ,
                      answer varchar(200) ,
                      option1 varchar(200) ,
                      option2 varchar(200) ,
                      option3 varchar(200) ,
                      option4 varchar(200) ,
                      option5 varchar(200)
                      )comment  = '%s'""" % (table_name, comment)
            # 执行语句
            self._cursor.execute(sql)
        except Exception as error:
            print("数据表创建失败：", error)
        else:
            print("数据表%s创建成功" % table_name)
            print("执行execute()方法后影响的行数为：%d" % self._cursor.rowcount)
        finally:
            print("create_table(%s,%s)函数执行完毕" % (table_name, comment))

    def select_data(self, question):  # 向数据库查询
        print("select_data(%s)函数开始执行" % question)
        try:
            # SQL 查询语句
            sql = "SELECT id FROM  %s \
                   WHERE question = '%s'" % (self._tableName, question)
            # 执行sql语句
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            # 打印结果
            if not result:
                res = False
            else:
                res = True
        except Exception as error:
            print("数据查询失败：", error)
            # 发生错误数据库回滚
            self._connect.rollback()
        else:
            print("查询成功", end='=>')
            print("执行execute()方法后影响的行数为：%d" % self._cursor.rowcount)
            return res
        finally:
            print("select_data()函数执行完毕", end='\n\n')
    @changeArgs
    def add_data(self, question, answer, option1='', option2='', option3='', option4='',
                 option5=''):  # 向数据库中插入数据,选项默认全为空
        print("add_data(%s)函数开始执行" % question)
        try:
            # SQL 插入语句
            sql = "INSERT INTO %s(question, answer, option1, option2, option3, option4, option5)\
                        VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (self._tableName, question, answer, option1, option2, option3, option4, option5)
            # 执行sql语句
            self._cursor.execute(sql)
            # 提交到数据库执行
            self._connect.commit()
        except Exception as error:
            print("数据插入失败：", error)
            # 发生错误数据库回滚
            self._connect.rollback()
        else:
            print("数据插入成功", end='=>')
            print("执行execute()方法后影响的行数为：%d" % self._cursor.rowcount)
        finally:
            print("add_data(%s)函数执行完毕" % answer)

    def export(self, table_name, output_path):
        count = self._cursor.execute('select * from ' + table_name)
        # print(self._cursor.lastrowid)
        print('数据总数：', count)
        # 重置游标的位置
        self._cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = self._cursor.fetchall()

        # 获取MYSQL里面的数据字段名称
        fields = self._cursor.description
        workbook = xlwt.Workbook()

        # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
        # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
        sheet = workbook.add_sheet(table_name, cell_overwrite_ok=True)

        # 写上字段信息
        for field in range(0, len(fields) - 1):
            sheet.write(0, field, fields[field + 1][0])

        # 获取并写入数据段信息
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields) - 1):
                sheet.write(row, col, u'%s' % results[row - 1][col + 1])

        workbook.save(output_path)


def list_to_excel(data, output_path):
    workbook = xlwt.Workbook()

    # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
    # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
    sheet = workbook.add_sheet('table_', cell_overwrite_ok=True)
    print("开始导出数据")
    # 写上字段信息
    try:
        col = 0
        for field in [0].keys():
            sheet.write(0, col, field)
            col += 1
        # 获取并写入数据段信息
        for row in range(1, len(data) + 1):
            sheet.write(row, 1, u'%s' % data[row]['title'])
            sheet.write(row, 0, u'%s' % data[row]['index'])
    except Exception as err:
        print('导出错误：', err)
    finally:
        print("数据导出完毕")
        workbook.save(output_path)


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
        for row in range(sheetOne.nrows):
            # print('问题=>',questionRow[row],'\n')
            respone['question'] = questionRow[row]
            # 获取答案个数
            for num in range(len(answerRow[row])):
                index = ord(answerRow[row][num]) - ord('?') \
                    if ord(answerRow[row][num]) - ord('?') < sheetOne.ncols else 2
                # print('答案'+str(num+1)+'=>',answerRow[row][num],sheetOne.row(row)[index].value)
                respone['answer'].append({"option": answerRow[row][num], "value": sheetOne.row(row)[index].value})
            data.append(respone)
        f.write(json.dumps(data).encode('utf-8'))
        f.close()
    except Exception as err:
        print('导出错误：', err)
    finally:
        print("数据导出完毕")


if __name__ == '__main__':
    mysql = MYSQL()
    mysql.connect_db(config=setting.DB_CONFIG)
    try:
        for it in mysql.show_table():
            print(it)
            mysql.export(it[0], r'%s\%s.xls' % (setting.EXPORT_PATH, it[1]))

    except Exception as err:
        print('运行错误：', err)
    finally:
        print('执行完毕')

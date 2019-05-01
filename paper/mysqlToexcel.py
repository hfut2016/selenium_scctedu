# __Desc__ = 从数据库中导出数据到excel数据表中
import xlwt
import pymysql
from paper import setting


class MYSQL:
    def __init__(self):
        pass

    def __del__(self):
        self._cursor.close()
        self._connect.close()
        print('数据库关闭成功')

    def connectDB(self, config):
        """
        连接数据库
        :return:
        """
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

        except Exception as err:
            print("数据库打开失败：", err)
        else:
            print("数据库打开成功")

    def show_table(self):
        """
        获取数据库表注释说明
        :return:
        """
        try:
            sql = """SELECT
                table_name 表名,
                table_comment 表说明
                FROM
                information_schema.TABLES
                WHERE
                table_schema = '{0}'
                ORDER BY
                table_name""".format(setting.DB_CONFIG_2['db'])
            self._cursor.execute(sql)
        except Exception as err:
            print("表查询失败：", err)
        else:
            print("表查询成功")
            return self._cursor.fetchall()

    def export(self, table_name, output_path):
        self._cursor = self._connect.cursor()
        count = self._cursor.execute('select * from ' + table_name)
        # print(self._cursor.lastrowid)
        print(count)
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
        for field in range(0, len(fields) - 1):  # 省去id列 少一列
            sheet.write(0, field, fields[field + 1][0])  # 省去id列 向左移一列

        # 获取并写入数据段信息
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields) - 1):  # 省去id列 少一列
                sheet.write(row, col, u'%s' % results[row - 1][col + 1])  # 省去id列 向左移一列

        workbook.save(output_path)


if __name__ == '__main__':
    mysql = MYSQL()
    mysql.connectDB(config=setting.DB_CONFIG_2)
    try:
        for it in mysql.show_table():
            print(it)
            mysql.export(it[0], r'%s\%s.xls' % (setting.EXPORT_PATH, it[1]))

    except Exception as err:
        print('运行错误：', err)
    finally:
        print('main执行完毕')

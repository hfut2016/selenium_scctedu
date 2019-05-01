from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib
import search

data = {'result': 'request not define'}
host = ('0.0.0.0', 10086)

workbook = search.openExcel()


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if '?' in self.path:
            # 如果带有参数
            self.queryString = urllib.parse.unquote(self.path.split('?', 1)[1])
            respone = {
                "kw": '',
                "question": "服务器错误",
                "answer": []
            }
            try:
                params = urllib.parse.parse_qs(self.queryString)
                respone = search.query(workbook=workbook, keyWord=params["kw"][0])
                print(respone)
            except Exception as err:
                print(err)
            finally:
                self.wfile.write(json.dumps(respone).encode('utf-8'))
        else:
            self.wfile.write(json.dumps(data).encode('utf-8'))

        return


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print('Starting server, listen at: %s:%s' % host)
    server.serve_forever()

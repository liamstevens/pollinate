from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import boto3
import datetime
import os


session = boto3.session(aws_access_key_id=os.environ['aws_id'], aws_secret_access_key=os.environ['aws_key'])
client = session.client("dynamodb",)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_POST(self):
        try:
            client.put_item(TableName='connections',Item={'nodeID':{'S':'0'},'connectionTime':{'S':datetime.now.strftime("%d/%m/%Y %H:%M:%S")}})



def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
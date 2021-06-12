from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import boto3
import datetime
import os
from get_docker_secret import get_docker_secret




class S(BaseHTTPRequestHandler):
    access_id = "AKIA2ZEQBPABD2OILGOT"

    access_key = "31+LaS+k87Lou4OwESHonriLmqToiA+ZEr8YJpT2"
    session = boto3.session.Session(aws_access_key_id=access_id, aws_secret_access_key=access_key)
    client = session.client("dynamodb",region_name="ap-southeast-2")
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            print("putting data")
            logging.info('Putting data...\n')
            self.client.put_item(TableName='connections',Item={'nodeID':{'S':'0'},'connectionTime':{'S':datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}})
            print("put data.")
            logging.info('Put data.\n')
        except Exception as e:
            logging.info(f"Could not put data: {e}\n")
            pass


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting httpd on {server_address}...\n")
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
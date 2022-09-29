#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
import os
from urllib import response

class MyWebServer(socketserver.BaseRequestHandler):
    base = "www"
    response = ""
    data = ""


                # if fullPath[-1] != "/":
                #     self.response = "HTTP/1.1 301 Moved permanently\r\ncontent-type: text/html\r\nlocation: http://127.0.0.1:8080/" + path + "\r\n"
                #     #test_deep_no_end
                #     self.request.sendall(bytearray(self.response,'utf-8'))
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("\nGot a request of: %s\n" % self.data)

        byteToString = str(self.data, "utf-8")
        dataSplit = byteToString.split("\r\n")
        requestData = dataSplit[0].split(" ")
        request = requestData[0]
        path = requestData[1]
        fullPath = self.base + path

        if request == "GET":
            fullPath = self.base + path
            if os.path.isdir(fullPath):
                if fullPath[-1] == "/":
                    header = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n"
                    with open(fullPath + ("" if fullPath[-1] == "/" else "/") + "index.html") as f:
                        data = f.read()
                        self.response = header + data
                else:
                    header = f"HTTP/1.1 301 Moved Permanently\r\ncontent-type: text/html\r\nlocation: localhost:8080{path}/\r\n"
                    self.response = header
                
            elif os.path.exists(fullPath):
                if ".html" in fullPath or path == "/":
                    header = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n"
                    if path == "/":
                        fullPath = self.base + "/index.html"
                #will i access other files?
                elif ".css" in fullPath:
                    header = "HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n"
                else:
                    self.response = "HTTP/1.1 404 PAGE NOT FOUND\r\ncontent-type: text/html\r\n\r\n"
                    self.request.sendall(bytearray(self.response,'utf-8'))
                    return 
                with open(fullPath, "r") as f:
                    data = f.read()
                
                self.response = header + data
            else:
                self.response = "HTTP/1.1 404 PAGE NOT FOUND\r\ncontent-type: text/html\r\n\r\n"
        else:
            self.response = "HTTP/1.1 405 Method Not Allowed\r\ncontent-type: text/html\r\n\r\n"
        self.request.sendall(bytearray(self.response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

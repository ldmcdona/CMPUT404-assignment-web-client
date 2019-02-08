#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
import pdb

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #print("type:", type(url))
        o = urllib.parse.urlparse(url)
        if o.path == "":
            z = "/"
        else:
            z = o.path
        x = o.netloc.split(":")
        #print("flag 1")
        #print(o)
        #print(x, type(x))
        if len(x) > 1:
            self.connect(x[0], int(x[1]))
        else:
            self.connect(x[0], 80)
        #print("flag 2")

        package = "GET " + z + " HTTP/1.1\r\nHost: " + x[0] + "\r\nAccept: */*\r\nConnection: close\r\n\r\n"

        #print("package:", package)
            
        self.sendall(package)

        #print("flag 3")

        answer = self.recvall(self.socket)
        #pdb.set_trace()

        #print("---")
        #print(o)
        #print("package:\n", package)
        #print("url:", url)
        #print("---")
        #print("GET")
        #print("---")
        #print("answer:",answer)
        #print("---")

        #Might wanna change the error check to something more general use
        if re.search("200 OK", answer) == None:
            code = 404
            body = ""
            if re.search("301 Moved Permanently", answer) != None:
                code = 301
            if re.search("302 Found", answer) != None:
                code = 302
        else:
            code = 200
            text = answer.split("\r\n\r\n")
            body = ""
            for i in range(len(text)):
                if i != 0:
                    body += text[i]
            #print("body:", body)
            #print("---")
            #body = text[1]

        #print("Code:", code)

        self.close()
        
        #code = 500
        #body = ""
        #print("---")
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        o = urllib.parse.urlparse(url)
        z = o.path
        x = o.netloc.split(":")        
        self.connect(x[0], int(x[1]))

        if args == None:
            package = "POST " + z + " HTTP/1.1\r\nHost:" + x[0] + "\r\nContent-Length:0\r\n\r\n"
        else:
            p = ""
            for item in args:
                p += item + "=" + args[item] + "&"
            p = p[:-1]
            q = len(p)
            #print("q", q)
            #print(p)
            package = "POST " + z + " HTTP/1.1\r\nHost:" + x[0] + "\r\nContent-Length:" + str(q) + "\r\n\r\n" + p
        self.sendall(package)

        answer = self.recvall(self.socket)
       
        #print("----")
        #print(args)
        #print("----")
        #print("POST")
        #print("----")
        #print(package)
        #print("----")
        #print(answer)
        #print("----")     

        #Might wanna change the error check to something more general use
        if re.search("200 OK", answer) == None:
            code = 404
            body = ""
            if re.search("301 Moved Permanently", answer) != None:
                code = 301
            if re.search("302 Found", answer) != None:
                code = 302
        else:
            code = 200
            text = answer.split("\r\n\r\n")
            body = ""
            for i in range(len(text)):
                if i != 0:
                    body += text[i]
            #print

        #print("Code:", code)

        self.close()
        
        #code = 500
        #body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))

#  coding: utf-8
import socketserver,os

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


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024).strip()
        if self.data:

        #print("Got a request of: %s\n" % self.data)
            req = self.data.decode().split()
            path=req[1]
            #Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
            if req[0]!="GET":
                self.request.send("HTTP/1.1 405 Method Not Allowed\r\n".encode())
                na="<html>\n<body>\n405 Method Not Allowed:http://127.0.0.1:8080"+path+"\n</body>\n</html>"
                cl="Content-Length: "+str(len(na))+"\r\n"
                self.request.send(cl.encode())
                self.request.send(b"Connection: close\r\n\r\n")
                self.request.send(na.encode())
            else:
                #The webserver can return index.html from directories (paths that end in /)
                #Secure: https://docs.python.org/2/library/os.path.html
                if path.endswith("/")and os.path.abspath("./www"+path).startswith(os.getcwd()+"/www"):

                    try:
                        content = open("./www"+path+"index.html",'r').read()
                        cl="Content-Length: "+str(len(content))+"\r\n"
                        self.request.send("HTTP/1.1 200 OK \r\n".encode())
                        #https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
                        self.request.send("Content-Type: text/html; charset=UTF-8 \r\n".encode())
                        self.request.send(cl.encode())
                        self.request.send(b"Connection: close\r\n\r\n")
                        self.request.send(content.encode())
                    except:
                        #The webserver can server 404 errors for paths not found
                        self.request.send("HTTP/1.1 404 Not Found \r\n".encode())
                        nf="<html>\n<body>\n404 Not Found:http://127.0.0.1:8080"+path+"\n</body>\n</html>"
                        cl="Content-Length: "+str(len(nf))+"\r\n"
                        self.request.send(cl.encode())
                        self.request.send(b"Connection: close\r\n\r\n")
                        self.request.send(nf.encode())
                else:
                    if not path.endswith(".css") and not path.endswith(".html"):
                        newpath="./www"+path+"/index.html"
                        #Must use 301 to correct paths such as http://127.0.0.1:8080/deep to http://127.0.0.1:8080/deep/ (path ending)
                        if os.path.exists(newpath) and os.path.abspath("./www"+newpath).startswith(os.getcwd()+"/www"):
                            content = open(newpath).read()
                            #print("EXIST")

                            location = "Location: http://127.0.0.1:8080"+ path+"/\r\n"
                            #location = "Location: http://127.0.0.1:8080/deep/index.html\r\n"
                            self.request.send(b"HTTP/1.1 301 Moved Permanently\r\n")
                            self.request.send(location.encode())
                            self.request.send(b"Connection: close\r\n\r\n")
                            #self.request.send(content.encode())
                        else:
                            self.request.send("HTTP/1.1 404 Not Found \r\n".encode())
                            nf="<html>\n<body>\n404 Not Found:http://127.0.0.1:8080"+path+"\n</body>\n</html>"
                            cl="Content-Length: "+str(len(nf))+"\r\n"
                            self.request.send(cl.encode())
                            self.request.send(b"Connection: close\r\n\r\n")
                            self.request.send(nf.encode())
                    else:
                        #The webserver supports mime-types for CSS
                        if path.endswith(".css"):
                            if os.path.exists("./www"+path) and os.path.abspath("./www"+path).startswith(os.getcwd()+"/www"):
                                content = open("./www"+path,'r').read()
                                cl="Content-Length: "+str(len(content))+"\r\n"
                                self.request.send("HTTP/1.1 200 OK \r\n".encode())
                                self.request.send("Content-Type: text/css; charset=UTF-8 \r\n".encode())
                                self.request.send(cl.encode())
                                self.request.send(b"Connection: close\r\n\r\n")
                                self.request.send(content.encode())
                            else:
                                self.request.send("HTTP/1.1 404 Not Found \r\n".encode())
                                nf="<html>\n<body>\n404 Not Found:http://127.0.0.1:8080"+path+"\n</body>\n</html>"
                                cl="Content-Length: "+str(len(nf))+"\r\n"
                                self.request.send(cl.encode())
                                self.request.send(b"Connection: close\r\n\r\n")
                                self.request.send(nf.encode())

                        elif path.endswith(".html"):
                            #The webserver supports mime-types for HTML
                            if os.path.exists("./www"+path) and os.path.abspath("./www"+path).startswith(os.getcwd()+"/www"):
                                content = open("./www"+path,'r').read()
                                cl="Content-Length: "+str(len(content))+"\r\n"
                                self.request.send("HTTP/1.1 200 OK\r\n".encode())
                                self.request.send("Content-Type: text/html; charset=UTF-8 \r\n".encode())
                                self.request.send(cl.encode())
                                self.request.send(b"Connection: close\r\n\r\n")
                                self.request.send(content.encode())
                            else:
                                self.request.send("HTTP/1.1 404 Not Found \r\n".encode())
                                nf="<html>\n<body>\n404 Not Found:http://127.0.0.1:8080"+path+"\n</body>\n</html>"
                                cl="Content-Length: "+str(len(nf))+"\r\n"
                                self.request.send(cl.encode())
                                self.request.send(b"Connection: close\r\n\r\n")
                                self.request.send(nf.encode())



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

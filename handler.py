#!/usr/bin/env python2

import urlparse
import string,cgi,time
from BaseHTTPServer import BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):

    tealist = []
    userlist = []
    state = "serveroff"

    def do_GET(self):
        try:
            if self.path.endswith(".tea"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()

                self.wfile.write("hey, today is the " + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                self.wfile.write("\n<br>\nThere's always time for a nice cup of tea.")
                return

            if self.path.endswith(".tea?SigningIn"):   #
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()

                self.wfile.write("Signing in " + str(time.localtime()[7]))
                self.wfile.write("Signing in at" + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                self.wfile.write("\n<br>\nah go on")
                return
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


    def do_POST(self):

            print "recieved post!"
            Time_Now = time.time()
            timelimit=10

            for entry in self.userlist:
                if entry[1]-Time_Now>timelimit:
                    self.userlist.remove(entry)
                    self.tealist.remove(entry)
                    
            print "users on system: ", self.userlist
            print "users who want tea:", self.tealist

            makeTeaNow=False
            if len(self.tealist)>(len(self.userlist)/2):
                makeTeaNow=True

            print "maketeanow?", makeTeaNow        
            global rootnode

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                    query=cgi.parse_multipart(self.rfile, pdict)
                    self.send_response(301)

	            upfilecontent = query.get('upfile')
	            print "filecontent", upfilecontent[0]
	            self.wfile.write("<HTML>POST OK.<BR><BR>");
	            self.wfile.write(upfilecontent[0]);
	    else:
                print "A user messaged the system:"

                if self.path.endswith(".tea?SigningIn"):   #
                
                    print "A user doesn't want tea:"
                
                    length = int(self.headers['Content-Length'])
                    post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))

                    for key, value in post_data.iteritems():

                        if len(self.userlist)>0:
                            if key=='user':
                                if not any(value[0] == x[0] for x in self.userlist):
                                    print "adding new entry to userlist:", [value[0], time.time()]
                                    newEntry = [value[0],time.time()]
                                    self.userlist.append(newEntry)
                                    self.wfile.write("Hello " + str(newEntry))
                                else:
                                    for entry in self.userlist:
                                        if key=='user'and entry[0] == value[0]:
                                            entry[1] = time.time()
                        else:
                            print "adding new entry to userlist:", [value[0], time.time()]
                            newEntry = [value[0],time.time()]
                            self.userlist.append(newEntry)
                            self.wfile.write("Hello " + str(newEntry))
                    
                        print "%s=%s" % (key, value[0])

                        for entry in self.tealist:
                            print "remove?",entry[0], value[0]
                            if entry[0] == value[0]:
                                print "removed an entry from the tea list"
                                self.tealist.remove(entry)
                    
                    self.send_header('Content-type',	'text/html')
                    self.wfile.write("Signing in " + str(time.localtime()[7]))
                    self.wfile.write("Signing in at" + str(time.localtime()[7]))
                    self.wfile.write(" day in the year " + str(time.localtime()[0]))
                    self.wfile.write("\n<br>\nah go on")

                    print "Users: ",self.userlist

                elif self.path.endswith(".tea?IwantTea"):

                    print "A user requested tea!"
                    self.send_header('Content-type',	'text/html')
                    length = int(self.headers['Content-Length'])
                    post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))

                    print "post_data", post_data.iteritems()

                    for key, value in post_data.iteritems():
                        print "checking if entry in tealist"
                        
                        if len(self.tealist)>0:
                            if key=='user':
                                if not any(value[0] == x[0] for x in self.tealist):
                                    print "adding new entry to tealist:", [value[0], time.time()]
                                    newEntry = [value[0],time.time()]
                                    self.tealist.append(newEntry)
                                    self.wfile.write("Still Tea for " + str(newEntry));
                                else:                                    
                                    #print "modifying entry in tealist:", [value[0], time.time()]
                                    for entry in self.tealist:
                                        if key=='user'and entry[0] == value[0]:
                                            entry[1] = time.time()
                        else:
                            print "adding new entry to tealist:", [value[0], time.time()]
                            newEntry = [value[0],time.time()]
                            self.tealist.append(newEntry)
                            self.wfile.write("Tea for " + str(newEntry));
                    
                if makeTeaNow:
                    self.wfile.write("time for tea!");
                else:
                    self.wfile.write("tea father?");

                self.send_response(200)
            
            return

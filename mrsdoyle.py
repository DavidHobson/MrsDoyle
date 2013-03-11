#!/usr/bin/env python2
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
import os
import time
from math import floor
gtk.gdk.threads_init()
import gobject
import pycurl
import argparse
import cStringIO
from os import curdir, sep
from handler import MyHandler
from BaseHTTPServer import HTTPServer


#Parameters
MIN_WORK_TIME = 60 * 10 # min work time in seconds

# Create a new hbox with an image and a label packed into it
# and return the box.

def xpm_label_box(parent, xpm_filename, label_text):
    # Create box for xpm and label
    box1 = gtk.HBox(False, 0)
    box1.set_border_width(2)

    # Now on to the image stuff
    image = gtk.Image()
    image.set_from_file(xpm_filename)

    # Create a label for the button
    label = gtk.Label(label_text)

    # Pack the pixmap and label into the box
    box1.pack_start(image, False, False, 3)
    box1.pack_start(label, False, False, 3)

    image.show()
    label.show()
    return box1

class MrsDoyle:
    def __init__(self, args):

	self.username = args.username
	self.host = args.host

	self.userlist = []
	self.tealist = []

	if self.username == 'mrsDoyle':
		self.isMrsDoyle()
		gtk.main_quit()
		
        self.state = "serveroff"
        self.icon=gtk.status_icon_new_from_file(self.icon_directory()+"serveroff.png")
        self.set_state(self.state)
        self.icon.set_tooltip("Idle")
        self.tick_interval=10 #number of seconds between each poll
        self.icon.connect('activate',self.icon_click)
        self.icon.connect('button-press-event',self.icon_click)
        self.icon.set_visible(True)
        self.start_working_time = 0
	self.signin = True
	self.wantTea = False

       # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Image'd Buttons!")
        # It's a good idea to do this for all windows.
        self.window.connect("destroy", lambda wid: gtk.main_quit())
        self.window.connect("delete_event", lambda a1,a2:gtk.main_quit())
        # Sets the border width of the window.
        self.window.set_border_width(10)
        # Create a new button
        button = gtk.Button()
        # Connect the "clicked" signal of the button to our callback
        button.connect("clicked", self.icon_click)
        # This calls our box creating function
        box1 = xpm_label_box(self.window, "info.xpm", "tea father?")
        # Pack and show all our widgets
        button.add(box1)
        box1.show()
        button.show()
        self.window.add(button)
        self.window.show()
        
    def format_time(self,seconds):
        minutes = floor(seconds / 60)
        if minutes > 1:
            return "%d minutes" % minutes
        else:
            return "%d minute" % minutes

    def set_state(self,state):

        self.state=state
        self.icon.set_from_file(self.icon_directory()+state+".png")

        if state == "serveroff":
            print "Where's mrs doyle?"
        if state == "teatime":
            print "there's always time for a nice cup of tea."
        if state == "serveron":
            print "Tea father?"
        if state == "wanttea":
            print "I want tea!"
            
    def on_delete_event(self, widget, event):
        self.hide()
        return True    

    def tray_activate(self, widget):
        self.present()

    def icon_directory(self):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep

    def icon_click(self,dummy):
        
        if self.state == "serveroff":
		self.contactserver(wanttea=False)
                #self.set_state("serveron")
        elif self.state == "serveron":
                #change state to want tea!
		self.contactserver(wanttea=True)
        elif self.state == "wanttea":
                #clicked on icon when wanted tea, reset tea wish.
		self.contactserver(wanttea=False)
        elif self.state == "teatime":
                #clicked on icon when teatime, reset tea wish.
		self.contactserver(wanttea=False)

    def firstcontactserver(self):
        self.contactserver(wanttea=False)

    def contactserver(self,wanttea=True):

	 	buf = cStringIO.StringIO()
                self.wantTea = wanttea

	    	try:
                    if self.wantTea:
		 	    c = pycurl.Curl()
		 	    c.setopt(c.URL,'http://'+self.host+':9999/index.tea?IwantTea')
			    c.setopt(c.POSTFIELDS, 'user='+self.username)
		 	    c.setopt(c.WRITEFUNCTION, buf.write)
		 	    c.perform()
                    else:
			    c = pycurl.Curl()
			    c.setopt(c.URL,'http://'+self.host+':9999/index.tea?SigningIn')
			    c.setopt(c.POSTFIELDS, 'user='+self.username)
			    c.setopt(c.WRITEFUNCTION, buf.write)
		            c.perform()

	     	except:
		    print "Mrs Doyle's gone"
		    self.set_state("serveroff")		                        

                print buf.getvalue()
	
		if buf.getvalue().find('time for tea')>-1:
			    self.set_state("teatime")
		else:
                    if self.wantTea:
		 	self.set_state("wanttea")
                    else:    
                        if buf.getvalue().find('ah go on')>-1:
                            self.set_state("serveron")
		 	else:
		 	    self.set_state("serveroff")

		buf.close()

    def isMrsDoyle(self): #run the server!
	try:
		server = HTTPServer(('', 9999), MyHandler)
		server.MrsDoyle = self
                server.MrsDoyle.state ="serveron"

		print "%s is Mrs Doyle" % server.MrsDoyle.username
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

    def update(self):
        """This method is called everytime a tick interval occurs"""
        delta = time.time() - self.start_working_time
        if self.state == "idle":
            pass
        else:
            self.icon.set_tooltip("Working for %s..." % self.format_time(delta))
            if self.state == "working":
                if delta > MIN_WORK_TIME:
                    self.set_state("ok")
                    
	print "Ah go on..."
	self.contactserver(wanttea=self.wantTea)

        source_id = gobject.timeout_add(self.tick_interval*250, self.update)

    def main(self):
        source_id = gobject.timeout_add(self.tick_interval, self.update)
        gtk.main()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some args.')
	parser.add_argument('--user', dest="username", help='persons name')
	parser.add_argument('--teamaker', dest="host", help='server name in dns')	
	args = parser.parse_args()
	app = MrsDoyle(args)
	app.main()


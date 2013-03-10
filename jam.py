import pycurl
import cStringIO
import urllib

print "1"
buf = None
buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL,'http://localhost:9999/index.tea')
c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

print "request:"
print buf.getvalue()
buf.close()

print "2"
buf = None
buf = cStringIO.StringIO()

user='dave'
client='jam'

data = {'user':'dave'}
data = urllib.urlencode(data)

c = pycurl.Curl()
c.setopt(c.URL,'http://localhost:9999/index.tea?SigningIn')
c.setopt(c.POSTFIELDS, data)
#c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

print "request:"
print buf.getvalue()
buf.close()

import time

time.sleep(4)

print "3"
buf = None
buf = cStringIO.StringIO()

user='dave'
client='jam'

data = {'user':'dave'}
data = urllib.urlencode(data)

c = pycurl.Curl()
c.setopt(c.URL,'http://localhost:9999/index.tea?IWantTea')
c.setopt(c.POSTFIELDS, data)
#c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

print "request:"
print buf.getvalue()
buf.close()

time.sleep(4)


print "4"
buf = None
buf = cStringIO.StringIO()

user='dave'
client='jam'

data = {'user':'dave'}
data = urllib.urlencode(data)

c = pycurl.Curl()
c.setopt(c.URL,'http://localhost:9999/index.tea?IWantTea')
c.setopt(c.POSTFIELDS, data)
#c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

print "request:"
print buf.getvalue()
buf.close()


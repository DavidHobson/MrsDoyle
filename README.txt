Introduction
============

MrsDoyle Tea App, for software geeks.

Running and installing
======================

This will need pycurl, pygtk, goobject, and setuptools will help.

(pycurl-7.19.0)

pycurl setup help:

Under OS x 10.7.5
Using python 2.7.
Depends on pycurl 7.19.0:  <download folder, in folder:> sudo python setup.py install
Test with python, import pycurl

This can use your local network DNS or any web server where you run the server, providing you have the correct host name used everywhere.

Running server:
python mrsdoyle.py --user mrsDoyle --teamaker <hostname>

Running clients:
python mrsdoyle.py --user <username> --teamaker <hostname>

Example client users would be 'Jack', 'Dougal', and 'Ted'.

Click the tea button to place a tea request. If more than 50% of all registered users request tea, the icons will change from green to red for all users, indicating teatime.

Clients have an icon and a control button that can be clicked.
The icon is grey when there is no server connection.
The icon is light green when server found.
The icon is bright green when that specific client requests tea.
The icon is red when the other clients vote for tea.

License
======================
Free to distribute under the terms of the GPLv3.
http://www.gnu.org/licenses/gpl-3.0.html

-By Dave 2012-2013.

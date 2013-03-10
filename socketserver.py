import SocketServer, subprocess, sys
from threading import Thread

my_unix_command = ['bc']
HOST = 'localhost'
PORT = 2000

def pipe_command(arg_list, standard_input=False):
    "arg_list is [command, arg1, ...], standard_input is string"
    pipe = subprocess.PIPE if standard_input else None
    print pipe
    print "arg_list",arg_list
    subp = subprocess.Popen(arg_list, stdin=pipe, stdout=subprocess.PIPE)
    print subp, dir(subp)
    print "standard_input",standard_input
    if not standard_input:
        return subp.communicate()[0]
    a = subp.communicate(standard_input)
    print a
    return a[0]

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        print "handling...", data
        reply = pipe_command(my_unix_command, data)
        print "reply:", reply
        if reply is not None:
            self.request.send(reply)
        self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

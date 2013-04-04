import sys
import socket
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class SimplerHTTPHandler (SimpleHTTPRequestHandler):
    """
    An even simpler HTTP request handler that returns
    the IP address of the server for all GET requests
    """
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('<h1 style="padding:50px;margin:100px auto 0 auto;width:400px;background-color:#eee;border:1px solid #ccc;font-family:Arial;text-align:center;">Served from ' + socket.gethostbyname(socket.gethostname()) + '</h1>\n');
        self.wfile.close()

HandlerClass = SimplerHTTPHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
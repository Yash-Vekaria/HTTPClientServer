# Import the server module
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import time


HOST = "173.230.149.18"
PORT = 23662
ROOT = "/var/www/html"


# Supporting multiple clients
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


# Handling the GET request
class GetHandler(BaseHTTPRequestHandler):
	
	# Generatign the response headers
	def do_HEAD(self, status_code, connection_object, content_type, content_length):

		self.send_response(status_code)

		if content_type == "html":
			self.send_header('Content-type', 'text/html')
		elif content_type == "text":
			self.send_header('Content-type', 'text/plain')
		elif content_type == "image":
			self.send_header('Content-type', 'image/jpeg')
		else:
			self.send_header('Content-type', 'unknown')

		if connection_object == "keep-alive":
			self.send_header('Connection', 'keep-alive')
		elif connection_object == "close":
			self.send_header('Connection', 'close')
		else:
			pass

		self.send_header('Content-length', str(content_length))
		self.end_headers()


	# Serving the GET request by generating appropriate response
	def do_GET(self):

		try:
			connection_type = str(self.headers['Connection'])
		
		except BaseException as e:
			connection_type = "None"

		if "X-Client-project" in self.headers and self.headers["X-Client-project"] == "project-152A-part2":
			
			################################### Generate Valid Response ###################################
			
			try:
				status_code, send_data, content_type = 200, bytes("","utf-8"), "text"
				
				if connection_type not in ["keep-alive", "close", "None"]:
					status_code, send_data, content_type = 400, bytes("Bad Request obtained! #1","utf-8"), "text"
				
				else:
					
					if '/images' in self.path:
						try:
							f = open(ROOT + self.path, "rb")
							send_data = f.read()
							f.close()
							status_code, content_type = 200, "image"
						
						except BaseException as e:
							status_code, send_data, content_type = 404, bytes("Requested Path Not Found #2","utf-8"), "text"
					
					elif self.path == "/ecs152a.html":
						f = open(ROOT + self.path, "r")
						content = f.read()
						f.close()
						status_code, send_data, content_type = 200, bytes(content,"utf-8"), "html"
					
					elif self.path == "/":
						status_code, send_data, content_type = 200, bytes("Request received successfully! #3","utf-8"), "text"
					
					else:
						status_code, send_data, content_type = 404, bytes("Requested Path Not Found #4","utf-8"), "text"
				
				contlen = len(send_data)
				self.do_HEAD(status_code, connection_type, content_type, contlen)
				
				################################################################################################
			
			except BaseException as e:
				send_data = "Bad Request obtained! #5 {}".format(e).encode()
				self.do_HEAD(400, connection_type, "text", len(send_data))
			
			finally:
				self.wfile.write(send_data)	
		
		else:
			send_data = "Bad Request obtained! #6".encode()
			self.do_HEAD(400, connection_type, "text", len(send_data))
			self.wfile.write(send_data)

		if connection_type in ["close"]:
			self.server.close_connection = True
		

if __name__ == '__main__':
	# from http.server import HTTPServer
	# server = HTTPServer((HOST, PORT), GetHandler)
	server = ThreadingSimpleServer((HOST, PORT), GetHandler)
	print('Starting server at http://%s:%s", use <Ctrl-C> to stop' % (HOST, PORT))
	server.request_queue_size = 10
	server.serve_forever()
import cgi
import http.server

ip = ''
port = 5555


class RequestHandler(http.server.SimpleHTTPRequestHandler):
		def do_GET(self):
			print("Get request received")
			self.send_response(200)
			self.send_header("Content-type","text/html")
			self.end_headers()
			self.wfile.write(bytes("<html><head><title>SimpleHTTP File Transfer</title></head>", "utf-8"))
			self.wfile.write(bytes("<body><p>Enter a filename.</p>", "utf-8"))
			self.wfile.write(bytes('<form action = "/" method = POST entype', "utf-8"))
			self.wfile.write(bytes('<input name = "foo"> <input type = filename = "bar">',"utf-8"))
			self.wfile.write(bytes('<input type = submit value = "List">',"utf-8"))
			self.wfile.write(bytes('<input type = submit value = "Get">',"utf-8"))
			self.wfile.write(bytes('<input type = submit value = "Put">',"utf-8"))
			self.wfile.write(bytes('<input type = submit value = "Delete">',"utf-8"))
			self.wfile.write(bytes("</body></html>", "utf-8"))
			
			print(self.path)
			return
			
		def do_POST(self):
			f = cgi.FieldStorage(headers=self.headers, fp=self.rfile, 
						environ = {"content-type": self.headers.get("content-type", "text/plain"),
						"Request_method": "POST"})
						
			if "bar" in f and f["bar"].file:
				f["bar"].filename
				f["bar"].fileread(1000)
			
try:
	srv = http.server.HTTPServer((ip, port), RequestHandler)
	print("Starting Server...")
	srv.serve_forever()
	
except KeyboardInterrupt:
	print("Shutting down web server")
	srv.socket.close()
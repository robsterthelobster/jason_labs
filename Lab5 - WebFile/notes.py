import http.server

class RH(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		self.path
		self.send_response(200)
		self.send_header("content_type", 0)
		self.end_header()
		self.wfile.write(-.0)
	def do_Post(self):
		f = cg.FieldStorare(headers=self.headers, fp=self.rfile,
						environ = {"content_tyupe": self.headers.get("content_type, "test/plain"),
						"Request_method": "POST"})

		<form action = "/" method = POST entype"
		<input name = "foo"> <input type = filename = "bar">
		<input type = submit>
		
		srv= http.server.HTTPServer((ip, port),RH)
		srv.serve_forever()
	
	

if "bar" in f and f["bar"].file:
	f["bar"].filename
	f["bar"].fileread(1000)
	
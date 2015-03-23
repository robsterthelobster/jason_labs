#!/usr/bin/env python3

import cherrypy
import mako.template
import mako.lookup
import os

lookup = mako.lookup.TemplateLookup(directories=["templates","."],strict_undefined=True)

class Server:
    
    @cherrypy.expose
    def index(self):
        tmp="""
        It works!<br>
        Click <a href="thing">me!</a><br>
        <img width=128 src="public/cat.png">
        Or, click <a href="public/jqtest.html">here</a>
        """
        return tmp
        
    @cherrypy.expose
    def thing(self):
        tmp = lookup.get_template("thing.html")
        return tmp.render(
            friend="John Doe", 
            people=["Alice","Bob","Carol"],
            people2=["Alice Smith","Bob Jones","Carol Piper"]
        )
    
s=Server()
cherrypy.config.update({
        #this only allows the local machine access to the server.
        #Change this to allow remote machines to access it.
        "server.socket_host": '127.0.0.1',
        "server.socket_port":1111
})

#any files under the local folder public-files 
#will appear on the web server under the URL /public
config = {
    "/public": {
        "tools.staticdir.on" : True,
        "tools.staticdir.dir" : os.path.abspath(os.path.join(".","public-files"))
    }
}

cherrypy.quickstart(s,'/',config)

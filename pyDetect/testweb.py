import os
import web
import subprocess
import logging
import sys
import datetime


urls = (
    '/REST/(.*)', 'rest',
)


class rest:
    # sample: http://<IP>:<PORT>/REST/terrasse?action=on
    def POST(self, name):
        i = web.input(action=None)
        print "got "
        print i

class MyOutputStream(object):
    def write(self, data):
        logging.debug(data)
        pass   # Ignore output
        
if __name__ == "__main__":

    sys.stdout = MyOutputStream()
    sys.stderr = MyOutputStream()

    app = web.application(urls, globals())
    logging.basicConfig(filename='web_serv.log',level=logging.DEBUG)
    app.run()

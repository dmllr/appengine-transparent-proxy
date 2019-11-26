import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, urlfetch_errors


def load_config():
    conf = dict()
    conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "endpoints.conf")
    with open(conf_path) as f:
        for line in f:
            endpoint, address = line.rstrip().split(' ')
            conf[endpoint] = address

    return conf


config = load_config()


class AllHandler(webapp.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    def proxy(self, endpoint, path):
        headers = self.request.headers
        headers.pop("Host", None)

        if endpoint not in config:
            self.error(404, "Endpoint not found in configuration file")
            return

        address = config[endpoint]

        try:
            response = urlfetch.fetch(
                address + path,
                self.request.body,
                self.request.method,
                self.request.headers,
                False, True,
                deadline=20)

            self.response.headers = response.headers
            self.response.write(response.content)
        except urlfetch_errors.Error as e:
            self.error(502, str(e))

    def head(self, endpoint, path):
        self.proxy(endpoint, path)

    def get(self, endpoint, path):
        self.proxy(endpoint, path)

    def post(self, endpoint, path):
        self.proxy(endpoint, path)

    def error(self, code, message):
        super(AllHandler, self).error(code)
        self.response.write('''
            <html>
             <head>
              <title>%d</title>
             </head>
             <body>
              <h1>%d</h1>
              %s
             </body>
            </html>
            ''' % (code, code, message))


def main():
    application = webapp.WSGIApplication([
        ('\/([a-zA-z0-9\-]*)(\/{0,1}.*)', AllHandler),
    ])

    run_wsgi_app(application)


if __name__ == "__main__":
    main()

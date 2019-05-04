import webapp2
from google.appengine.ext import blobstore


class GenFile(webapp2.RequestHandler):
    def get(self):
        self.response.write(blobstore.create_upload_url('/upload'))

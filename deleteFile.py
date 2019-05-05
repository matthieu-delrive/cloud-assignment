import webapp2
import logging
import json
from google.appengine.api import users
from google.appengine.ext import ndb

from models.directories import Directories


class DeleteFile(webapp2.RequestHandler):
    # deletefile by id
    def get(self):
        self.response.headers['Content-Type'] = 'text/json'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        try:
            id_file = int(self.request.get('id'))
            delete_file = ndb.Key('Files', id_file)
        except ValueError:
            delete_file = None
        if user and delete_file and delete_file.get().userOwner == myuser_key:
            name = delete_file.get().filenames
            delete_file.delete()
            self.response.write(json.dumps({"delete": name}))
        else:
            logging.info('error')
            self.response.set_status(403)
            self.response.write(json.dumps({"error": "cannot delete file"}))

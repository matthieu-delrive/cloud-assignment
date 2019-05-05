import webapp2
import jinja2
import os
import logging
import json
from google.appengine.api import users
from google.appengine.ext import ndb

from models.directories import Directories


class DeleteDirectory(webapp2.RequestHandler):
    # delete directory by id
    def get(self):
        self.response.headers['Content-Type'] = 'text/json'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        try:
            id_directory = int(self.request.get('id'))
            directory = ndb.Key('Directories', id_directory)
        except ValueError:
            directory = None
        if user and directory and directory.get().parent_directory is not None and directory.get().userOwner == myuser_key:
            name = directory.get().name
            allsub = Directories.query(Directories.parent_directory == directory).fetch()
            for i in allsub:
                i.key.delete()
            directory.delete()
            self.response.write(json.dumps({"delete": name}))
        else:
            logging.info('error')
            self.response.set_status(403)
            self.response.write(json.dumps({"error": "cannot detete directory"}))

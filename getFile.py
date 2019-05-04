import webapp2
import logging
import json
from google.appengine.api import users
from google.appengine.ext import ndb

from models.files import Files


class GetFile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/json'
        user = users.get_current_user()
        try:
            id_directory = int(self.request.get('id'))
            directory = ndb.Key('Directories', id_directory)
        except ValueError:
            directory = None
        if user and directory:
            myuser_key = ndb.Key('MyUser', user.user_id())
            ls = Files.query(
                Files.directory == directory).fetch()

            js = []
            for i in ls:
                js.append({"id": i.key.id(), "name": i.filenames, "size": i.size, "typefile": i.typeFile,
                           "creationdate": i.creationDate})
            self.response.write(json.dumps(js))
        else:
            logging.info('error')
            self.response.set_status(403)
            self.response.write(json.dumps({"error": "cannot fetch data"}))

import webapp2
import logging
import json
from google.appengine.api import users
from google.appengine.ext import ndb

from models.directories import Directories


class Directory(webapp2.RequestHandler):
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
            ls = Directories.query(
                Directories.parent_directory == directory).fetch()
            js = []
            for i in ls:
                js.append({"id": i.key.id(), "name": i.name})
            self.response.write(json.dumps(js))
        else:
            logging.info('error')
            self.response.set_status(403)
            self.response.write(json.dumps({"error": "cannot fetch data"}))

    def post(self):
        body = json.loads(self.request.body)
        user = users.get_current_user()
        if user and 'parent_id' in body and 'name' in body:
            try:
                parent_directory = ndb.Key('Directories', int(body['parent_id']))
            except ValueError:
                parent_directory = None
            if parent_directory:
                myuser_key = ndb.Key('MyUser', user.user_id())
                if parent_directory.get().userOwner == myuser_key:
                    # ls = Directories.query_directory_in_parent(parent_directory)
                    ls = Directories.query(
                        Directories.parent_directory == parent_directory, Directories.name == body['name']).get()
                    if ls is None:
                        directory = Directories(name=body['name'], userOwner=myuser_key,
                                                parent_directory=parent_directory)
                        directory.put()
                        return self.response.write(json.dumps([{"name": directory.name, "_id": directory.key.id()}]))

        logging.info('error cannot add new directory')
        self.response.set_status(403)
        self.response.write({"error": "cannot add new directory"})

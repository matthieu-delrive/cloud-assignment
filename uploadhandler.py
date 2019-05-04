import json

from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from models.files import Files
from google.appengine.ext.webapp import blobstore_handlers
import datetime


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/json'
        user = users.get_current_user()
        try:
            id_directory = int(self.request.get('id'))
            directory = ndb.Key('Directories', id_directory)
        except ValueError:
            directory = None
        if user and directory:
            myuser_key = ndb.Key('MyUser', user.user_id())

            upload = self.get_uploads()[0]
            blobinfo = blobstore.BlobInfo(upload.key())
            filename = blobinfo.filename
            size = blobinfo.size
            typefile = blobinfo.content_type
            now = datetime.datetime.now()

            file_created = Files(filenames=filename, userOwner=myuser_key,
                                 directory=directory, blob=upload.key(),
                                 size=size, typeFile=typefile, creationDate=now.strftime("%Y-%m-%d %H:%M"))
            file_created.put()
            self.response.write(json.dumps([{"name": file_created.filenames, "_id": file_created.key.id(), "size": size,
                                             "typefile": typefile, "creationdate": now.strftime("%Y-%m-%d %H:%M")}]))
        else:
            self.response.set_status(403)
            self.response.write({"error": "cannot add new file"})

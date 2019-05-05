from google.appengine.ext import ndb

from models import directories


# file model
class Files(ndb.Model):
    # email address of this user
    directory = ndb.KeyProperty(kind="Directories")
    filenames = ndb.StringProperty()
    blob = ndb.BlobKeyProperty()
    userOwner = ndb.KeyProperty(kind="MyUser")
    size = ndb.IntegerProperty()
    typeFile = ndb.StringProperty()
    creationDate = ndb.StringProperty()

from google.appengine.ext import ndb

from models.directories import Directories


# model user
class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    directory = ndb.KeyProperty(kind="Directories")

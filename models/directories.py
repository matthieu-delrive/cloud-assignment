from google.appengine.ext import ndb


# directory model
class Directories(ndb.Model):
    # email address of this user

    name = ndb.StringProperty()
    parent_directory = ndb.KeyProperty(kind='Directories')
    userOwner = ndb.KeyProperty(kind='MyUser')

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from deleteFile import DeleteFile
from downloadHandler import DownloadHandler
from genFile import GenFile
from getFile import GetFile
from models.myuser import MyUser
from models.directories import Directories

from directory import Directory
from delete_directory import DeleteDirectory
from uploadhandler import UploadHandler

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'], autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        global myuser
        self.response.headers['Content-Type'] = 'text/html'
        welcome = 'Welcome back'
        directory = None
        directory_id = ""
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            if myuser is None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.email_address = user.email()
                directory = Directories(name=user.email(), userOwner=myuser.key)
                directory.put()
                myuser.directory = directory.key
                myuser.put()
                directory_id = directory.key.id()

            else:
                directory = myuser.directory.get()
            directory_id = directory.key.id()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {'url': url, 'url_string': url_string, 'user': user, 'welcome': welcome, 'directory': directory, 'directory_id': directory_id}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/directory', Directory),
                               ('/delete-directory', DeleteDirectory),
                               ('/delete-file', DeleteFile),
                               ('/get-files', GetFile),
                               ('/gen-file', GenFile),
                               ('/upload', UploadHandler),
                               ('/download', DownloadHandler),
                               ], debug=True)

if __name__ == '__main__':
    app.run()

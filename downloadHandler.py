
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    # download handler send the file for download
    def get(self):
        index = int(self.request.get('id'))
        self.response.headers['Content-Type'] = 'application/x-gzip'

        collection_key = ndb.Key('Files', index)
        collection = collection_key.get()
        self.response.headers['Content-Disposition'] = 'attachment; filename=%s' % str(collection.filenames)
        self.send_blob(collection.blob)

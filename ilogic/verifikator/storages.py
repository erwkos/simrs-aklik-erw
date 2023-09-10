from django.core.files.storage import Storage, DefaultStorage, FileSystemStorage


class TemporaryStorage(FileSystemStorage):
    location = '/tmp/import_export/'

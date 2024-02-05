class ProgressVersionRouter:
    integrasi_db = 'integrasi'
    default_db = 'default'

    def db_for_read(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'progressversion':
            return self.integrasi_db
        if model_name == 'polarules':
            return self.integrasi_db
        return self.default_db

    def db_for_write(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'progressversion':
            return self.integrasi_db
        if model_name == 'polarules':
            return self.integrasi_db
        return self.default_db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'progressversion':
            return db == self.integrasi_db
        if model_name == 'polarules':
            return db == self.integrasi_db
        return db == self.default_db

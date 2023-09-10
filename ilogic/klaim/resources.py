from import_export import resources

from klaim.models import DataKlaimCBG


class DataKlaimCBGResource(resources.ModelResource):

    class Meta:
        model = DataKlaimCBG
        import_id_fields = ('NOSEP', )
        fields = ('status', 'NOSEP')
        skip_unchanged = True
        use_bulk = True
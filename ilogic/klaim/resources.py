from import_export import resources, fields

from import_export.widgets import ManyToManyWidget

from klaim.models import DataKlaimCBG, KeteranganPendingDispute


class DataKlaimCBGResource(resources.ModelResource):

    class Meta:
        model = DataKlaimCBG
        import_id_fields = ('NOSEP', )
        fields = ('status', 'NOSEP', 'jenis_pending', 'jenis_dispute')
        skip_unchanged = True
        use_bulk = True



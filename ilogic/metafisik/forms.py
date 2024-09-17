from django import forms


class ImportDataKlaimCBGMetafisikForm(forms.Form):
    file = forms.FileField(label='Upload File Excel', required=True,
                           help_text='Hanya menerima file dengan ekstensi `.xlsx` dan ukuran maksimal')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file.name.split('.')[-1] != 'xlsx':
            raise forms.ValidationError('Hanya menerima file dengan ekstensi `.xlsx`')
        return file


class DataKlaimCBGMetafisikForm(forms.Form):
    kode_ppk = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))
    # tanggal_pelayanan = forms.DateField(widget=forms.DateInput(attrs={'type': 'hidden'}))
    month_tanggal_pengajuan = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'hidden'}))
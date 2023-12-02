from django import forms 
from .models import Traceroute

class TracerouteForm(forms.Form):
    class Meta:
        ip_address = forms.GenericIPAddressField(label='Endereço IP', max_length=50)
        ttl = forms.IntegerField(label='Numero de saltos (TTL)', min_value=1, max_value=255)

        model = Traceroute

        exclude = ['icmp_type',
                   'icmp_code',
                   'remote_machine',
                   'protocol',
                   ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    
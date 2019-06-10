from django import forms
from books_app.models import *

from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget

class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }



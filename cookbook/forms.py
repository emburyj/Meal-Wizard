from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime

class new_recipe_collection_form(forms.Form):
        box = forms.BooleanField(required=False)

class new_rc_date_form(forms.Form):
    date = forms.DateField(widget=AdminDateWidget,label="Meal Plan Start Date", initial=datetime.now, required=True)
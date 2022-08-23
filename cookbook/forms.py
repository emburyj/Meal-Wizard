from django import forms

from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime

class new_recipe_collection_form(forms.Form):
        box = forms.BooleanField(required=False)

class new_rc_date_form(forms.Form):
    date = forms.DateField(widget=AdminDateWidget,label="Meal Plan Start Date", initial=datetime.now, required=True)

class new_recipe_form(forms.Form):
    name = forms.CharField(label = "Recipe Name", max_length=128)
    list_of_choices = ((1, 'Salad'), (2, 'Soup'), (3, 'Pasta'), (4, 'Curry'),
     (5, 'Pizza'), (6, 'Brunch'),(7, 'Other'))
    rec_type = forms.ChoiceField(choices=list_of_choices)

class new_recipe_ingredients_form(forms.Form):
    ingred = forms.CharField(label="", max_length=128, required=False)
    qty = forms.IntegerField(label="", min_value=0, max_value=10, required=False)
    # add a bunch of ingredient inputs (10?)
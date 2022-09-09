from django import forms

from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime

# class MyButtonInput(forms.widgets.CheckboxInput):
#     input_type = 'button'


class new_recipe_collection_form(forms.Form):
        box = forms.BooleanField(required=False)#, widget=MyButtonInput(attrs={'class': 'btn btn-primary-bg btn-lg btn-outline-dark',
         #'type':'button', 'data-bs-toggle': 'button', 'aria-pressed': 'true', 'label':'something'}))


class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'

class new_rc_date_form(forms.Form):
    date = forms.DateField(widget=MyDateInput(),label="Meal Plan Start Date", initial=datetime.now, required=True)

rec_type_choices = ((1, 'Salad'), (2, 'Soup'), (3, 'Pasta'), (4, 'Curry'),
 (5, 'Pizza'), (6, 'Brunch'),(7, 'Other'))

class new_recipe_form(forms.Form):
    name = forms.CharField(label = "Recipe Name", max_length=128)
    rec_type = forms.ChoiceField(choices=rec_type_choices, label="Recipe Type")

ing_type_choices = ((0, ""), (1, "Meat"), (2, "Produce"), (3,"Dairy"), (4, "Grain"),
 (5, "Pasta"), (6, "Canned"), (7, "Condiment"), (8, "Other"))

class new_recipe_ingredients_form(forms.Form):
    ingred = forms.CharField(label="", max_length=128, required=False)
    qty = forms.IntegerField(label="", min_value=0, max_value=10, required=False)
    ing_type = forms.ChoiceField(label = "", choices=ing_type_choices, required=False)
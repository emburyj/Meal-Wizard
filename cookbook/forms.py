from django import forms

class new_recipe_collection_form(forms.Form):
        box = forms.BooleanField(required=False)
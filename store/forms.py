from django import forms


class PallyCreationForm(forms.Form):
    max_no_of_people = forms.IntegerField(min_value=2)

class SingleOrderCreationForm(forms.Form):
    no_of_orders = forms.IntegerField(min_value=1)
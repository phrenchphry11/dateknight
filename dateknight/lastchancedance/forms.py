from django import forms


class AddCrush(forms.Form):
    chicken = forms.EmailField(label="Carleton email address", required=True)

class DeleteCrush(forms.Form):
    chicken = forms.EmailField(label="Carleton email address", required=True)


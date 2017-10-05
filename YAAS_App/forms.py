from django import forms


class CreateAuction(forms.Form):
    title=forms.CharField(required=True)
    description=forms.CharField(widget=forms.Textarea(),required=True)
    start_price=forms.DecimalField(max_digits=6,decimal_places=2)
    endtime=forms.DateTimeField(required=True)

class ConfirmAuction(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES)
    t_title = forms.CharField(widget=forms.HiddenInput())

class Searchingform(forms.Form):
    searc=forms.CharField(label='Enter a word to search for',
    widget=forms.TextInput(attrs={'size':25}))

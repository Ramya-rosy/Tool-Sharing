from django import forms

from listings.models import Listing

class listingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(listingForm, self).__init__(*args, **kwargs)
        self.fields['borrow_duration'].widget.attrs['min'] = 1
        self.fields['borrow_duration'].label = "Borrow duration (Days):"

    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['user']
        # widgets = {
        #     'availablity_date': forms.widgets.DateInput(attrs={'type': 'date'})
        # }

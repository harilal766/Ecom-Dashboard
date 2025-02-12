from django import forms


css_attributes = {
    "class" : "form-control"
    }

store_options = [
        ("","Select a platform"),
        ("Amazon","Amazon"),
        ("Shopify","Shopify")
    ]


class Addstoreform(forms.Form):
    
    store_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs = 
        {**css_attributes,"id":"storeName","placeholder":"Enter the store name"}))
    platform = forms.ChoiceField(choices=store_options,label="Select the platform",widget=forms.Select(attrs=
        {**css_attributes,"id":"storePlatform"}))













from store.models import Product, Pally
from .models import Vendor
from django import forms


class VendorRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = " ".join([css, "form-control mb-3"]).strip()
            if "placeholder" not in field.widget.attrs:
                field.widget.attrs["placeholder"] = field.label



    class Meta:
        model = Vendor
        exclude = ('user',)

class AddProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        custom_widgets = [forms.CheckboxInput, forms.RadioSelect]
        for field_name, field in self.fields.items():
            if field.widget.__class__ in custom_widgets:
                css = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = ""
            else:
                css = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = " ".join([css, "form-control"]).strip()
                if "placeholder" not in field.widget.attrs:
                    field.widget.attrs["placeholder"] = field.label
            if isinstance(field, forms.models.ModelMultipleChoiceField):
                field.widget = forms.CheckboxSelectMultiple(choices=field.choices)
                

    class Meta:
        model = Product
        exclude = ('vendor', 'created', 'updated', 'slug')

# class AddPallyForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         for field_name, field in self.fields.items():
#             if isinstance(field, forms.models.ModelMultipleChoiceField):
#                 field.widget = forms.CheckboxSelectMultiple(choices=field.choices)
#             css = field.widget.attrs.get("class", "")
#             field.widget.attrs["class"] = " ".join([css, "form-control mb-3"]).strip()
#             if "placeholder" not in field.widget.attrs:
#                 field.widget.attrs["placeholder"] = field.label

#     class Meta:
#         model = Pally
#         exclude = ('vendor', 'created', 'updated', 'slug')
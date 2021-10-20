from django import forms
from general.models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = " ".join([css, "form-control mb-3"]).strip()
            if "placeholder" not in field.widget.attrs:
                field.widget.attrs["placeholder"] = field.label

    class Meta:
        model = ContactRequest
        fields = "__all__"

from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "company_name", "domain", "industry", "employee_count",
            "estimated_revenue", "contact_name", "email", "location", "source", "notes",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "e.g. Acme Manufacturing"}),
            "domain": forms.TextInput(attrs={"placeholder": "example.com"}),
            "industry": forms.TextInput(attrs={"placeholder": "Manufacturing"}),
            "estimated_revenue": forms.NumberInput(attrs={"min": "0", "step": "0.01", "placeholder": "Annual revenue (optional)"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_company_name(self):
        value = self.cleaned_data["company_name"].strip()
        if not value:
            raise forms.ValidationError("Company name is required.")
        return value

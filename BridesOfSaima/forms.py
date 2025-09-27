from django import forms
from django.forms import inlineformset_factory
from .models import Customer, Invoice, InvoiceItem
from datetime import date, timedelta

class CustomerForm(forms.ModelForm):
    """Form for customer information"""
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter customer address'
            }),
        }

class InvoiceForm(forms.ModelForm):
    """Form for invoice details"""
    class Meta:
        model = Invoice
        fields = ['customer', 'issue_date', 'due_date', 'payment_status', 'discount_percentage', 'tax_percentage', 'advance_amount', 'notes']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            }),
            'tax_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            }),
            'advance_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes or terms'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default dates
        if not self.instance.pk:
            self.fields['issue_date'].initial = date.today()
            self.fields['due_date'].initial = date.today() + timedelta(days=30)

class InvoiceItemForm(forms.ModelForm):
    """Form for invoice line items"""
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item description'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '1'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
        }

# Create formset for invoice items
InvoiceItemFormSet = inlineformset_factory(
    Invoice, 
    InvoiceItem, 
    form=InvoiceItemForm,
    extra=2,  # Number of empty forms to display
    can_delete=True,
    min_num=1,  # Minimum number of forms required
    validate_min=True
)
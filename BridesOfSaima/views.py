from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Invoice, Customer, InvoiceItem, Bride
from .forms import InvoiceForm, InvoiceItemFormSet, CustomerForm

def is_staff_user(user):
    """Check if user is staff/admin"""
    return user.is_authenticated and user.is_staff

# Create your views here.

def homepage(request):
    """
    Homepage view for BridesOfSaima app
    """
    return render(request, 'BridesOfSaima/homepage.html')

def invoice_list(request):
    """
    Display list of all invoices
    """
    invoices = Invoice.objects.all().select_related('customer')
    return render(request, 'BridesOfSaima/invoice_list.html', {
        'invoices': invoices
    })

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def invoice_create(request):
    """
    Create a new invoice (Admin only)
    """
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        
        if invoice_form.is_valid():
            with transaction.atomic():
                invoice = invoice_form.save()
                formset = InvoiceItemFormSet(request.POST, instance=invoice)
                
                if formset.is_valid():
                    formset.save()
                    messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
                    return redirect('BridesOfSaima:invoice_detail', pk=invoice.pk)
                else:
                    invoice.delete()  # Rollback invoice creation if items are invalid
                    messages.error(request, 'Please correct the errors in invoice items.')
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet()
    
    return render(request, 'BridesOfSaima/invoice_form.html', {
        'invoice_form': invoice_form,
        'formset': formset,
        'title': 'Create New Invoice'
    })

def invoice_detail(request, pk):
    """
    Display invoice details
    """
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'BridesOfSaima/invoice_detail.html', {
        'invoice': invoice
    })

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def invoice_edit(request, pk):
    """
    Edit existing invoice (Admin only)
    """
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        
        if invoice_form.is_valid():
            with transaction.atomic():
                invoice = invoice_form.save()
                formset = InvoiceItemFormSet(request.POST, instance=invoice)
                
                if formset.is_valid():
                    formset.save()
                    messages.success(request, f'Invoice {invoice.invoice_number} updated successfully!')
                    return redirect('BridesOfSaima:invoice_detail', pk=invoice.pk)
                else:
                    messages.error(request, 'Please correct the errors in invoice items.')
    else:
        invoice_form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    
    return render(request, 'BridesOfSaima/invoice_form.html', {
        'invoice_form': invoice_form,
        'formset': formset,
        'title': 'Edit Invoice',
        'invoice': invoice
    })

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def customer_create(request):
    """
    Create a new customer (Admin only)
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.name} created successfully!')
            return redirect('BridesOfSaima:invoice_create')
        else:
            messages.error(request, 'Please correct the errors in customer form.')
    else:
        form = CustomerForm()
    
    return render(request, 'BridesOfSaima/customer_form.html', {
        'form': form,
        'title': 'Add New Customer'
    })

def invoice_print(request, pk):
    """
    Generate printable invoice
    """
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'BridesOfSaima/invoice_print.html', {
        'invoice': invoice
    })

def brides_gallery(request):
    """
    Display gallery of all brides
    """
    brides = Bride.objects.all().order_by('-event_date', '-created_at')
    return render(request, 'BridesOfSaima/brides_gallery.html', {
        'brides': brides,
        'title': 'My Brides Gallery'
    })

def bride_detail(request, pk):
    """Display detailed view of a bride with carousel of all images"""
    bride = get_object_or_404(Bride, pk=pk)
    all_images = bride.get_all_images()
    
    return render(request, 'BridesOfSaima/bride_detail.html', {
        'bride': bride,
        'all_images': all_images,
        'total_images': len(all_images)
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Invoice, Customer, InvoiceItem, Bride
from .forms import InvoiceForm, InvoiceItemFormSet, CustomerForm, BrideForm

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
def customer_list(request):
    """
    Display list of all customers (Admin only)
    """
    customers = Customer.objects.all().order_by('name')
    return render(request, 'BridesOfSaima/customer_list.html', {
        'customers': customers,
        'title': 'Customer List'
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
            return redirect('BridesOfSaima:customer_list')
        else:
            messages.error(request, 'Please correct the errors in customer form.')
    else:
        form = CustomerForm()
    
    return render(request, 'BridesOfSaima/customer_form.html', {
        'form': form,
        'title': 'Add New Customer'
    })

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def customer_edit(request, pk):
    """
    Edit existing customer (Admin only)
    """
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.name} updated successfully!')
            return redirect('BridesOfSaima:customer_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'BridesOfSaima/customer_form.html', {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}'
    })

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def reports_dashboard(request):
    """
    Reports dashboard for bookings and income analysis (Admin only)
    """
    try:
        from django.db.models import Sum, Count, Q
        from datetime import datetime, date
        import calendar
        import json
        
        # Get filter parameters
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        # Convert to integers if provided, otherwise keep as None for "All" filter
        current_date = date.today()
        if month:
            try:
                month = int(month)
            except ValueError:
                month = None
        else:
            month = None
        
        if year:
            try:
                year = int(year)
            except ValueError:
                year = None
        else:
            year = None
        
        # Base queryset for invoices
        invoices = Invoice.objects.all()
        
        # Apply filters only if specified (otherwise show all data)
        if month and year:
            invoices = invoices.filter(
                issue_date__year=year,
                issue_date__month=month
            )
        elif year and not month:
            invoices = invoices.filter(issue_date__year=year)
        elif month and not year:
            # If only month is selected, show that month for all years
            invoices = invoices.filter(issue_date__month=month)
        
        # Calculate statistics using invoice methods
        total_bookings = invoices.count()
        total_advance_result = invoices.aggregate(total=Sum('advance_amount'))
        total_advance = float(total_advance_result['total'] or 0)
        
        # Calculate total revenue and due amounts using invoice methods
        total_revenue = 0
        total_due = 0
        for invoice in invoices:
            try:
                total_revenue += float(invoice.get_total())
                total_due += float(invoice.get_due_amount())
            except (TypeError, ValueError, AttributeError):
                # Handle potential conversion errors
                continue
        
        # Payment status breakdown
        paid_invoices = invoices.filter(payment_status='paid').count()
        pending_invoices = invoices.filter(payment_status='pending').count()
        partial_invoices = invoices.filter(payment_status='partially_paid').count()
        
        # Monthly data for chart (last 12 months) - simplified version
        monthly_data = []
        
        # If no specific year is selected, use current year for chart
        chart_year = year if year else current_date.year
        
        # Generate data for all 12 months of the selected/current year
        for month_num in range(1, 13):
            try:
                month_invoices = Invoice.objects.filter(
                    issue_date__year=chart_year,
                    issue_date__month=month_num
                )
                
                # Calculate monthly totals
                monthly_revenue = 0
                monthly_advance = 0
                for invoice in month_invoices:
                    try:
                        monthly_revenue += float(invoice.get_total())
                        monthly_advance += float(invoice.advance_amount or 0)
                    except (TypeError, ValueError, AttributeError):
                        continue
                
                monthly_data.append({
                    'month': calendar.month_name[month_num],
                    'year': chart_year,
                    'bookings': month_invoices.count(),
                    'revenue': round(monthly_revenue, 2),
                    'advance': round(monthly_advance, 2)
                })
                    
            except Exception:
                # Skip this month if there's an error
                continue
        
        # Recent invoices with calculated totals
        recent_invoices = invoices.select_related('customer').order_by('-issue_date')[:10]
        
        # Add calculated fields to invoices for template
        invoices_with_totals = []
        for invoice in invoices.select_related('customer').order_by('-issue_date'):
            try:
                invoice.total_amount = float(invoice.get_total())
                invoice.due_amount = float(invoice.get_due_amount())
                invoices_with_totals.append(invoice)
            except (TypeError, ValueError, AttributeError):
                # Skip invoices with calculation errors
                continue
        
        # Generate month/year options for filters
        years = list(range(2020, current_date.year + 2))
        months = [(i, calendar.month_name[i]) for i in range(1, 13)]
        
        context = {
            'title': 'Bookings & Income Report',
            'selected_month': month,
            'selected_year': year,
            'month_name': calendar.month_name[month] if month else 'All Months',
            'months': months,
            'years': years,
            'total_bookings': total_bookings,
            'total_revenue': round(total_revenue, 2),
            'total_advance': round(total_advance, 2),
            'total_due': round(total_due, 2),
            'paid_invoices': paid_invoices,
            'pending_invoices': pending_invoices,
            'partial_invoices': partial_invoices,
            'monthly_data': monthly_data,
            'recent_invoices': recent_invoices,
            'invoices': invoices_with_totals
        }
        
        # For debugging, use the debug template first
        # return render(request, 'BridesOfSaima/reports_debug.html', context)
        return render(request, 'BridesOfSaima/reports_dashboard.html', context)
        
    except Exception as e:
        # Fallback error handling with debug info
        from django.contrib import messages
        import traceback
        error_details = traceback.format_exc()
        messages.error(request, f'Error loading reports: {str(e)}')
        # In development, you might want to print or log the error details
        print(f"Reports Error: {error_details}")
        return redirect('BridesOfSaima:homepage')

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

@user_passes_test(is_staff_user, login_url='/accounts/login/')
def bride_edit(request, pk):
    """Edit existing bride (Admin only)"""
    bride = get_object_or_404(Bride, pk=pk)
    
    if request.method == 'POST':
        form = BrideForm(request.POST, request.FILES, instance=bride)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bride {bride.name} updated successfully!')
            return redirect('BridesOfSaima:brides_gallery')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = BrideForm(instance=bride)
    
    return render(request, 'BridesOfSaima/bride_edit.html', {
        'form': form,
        'bride': bride,
        'title': f'Edit {bride.name}'
    })

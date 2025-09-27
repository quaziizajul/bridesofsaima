from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

# Create your models here.

class Bride(models.Model):
    """Model for showcasing brides gallery"""
    name = models.CharField(max_length=200, help_text="Bride's name")
    location = models.CharField(max_length=200, help_text="Wedding/event location")
    event_date = models.DateField(help_text="Date of the makeup/event")
    tagline = models.CharField(max_length=300, help_text="Special tagline or description")
    image = models.ImageField(upload_to='brides/', help_text="Main bride photo for gallery thumbnail")
    is_featured = models.BooleanField(default=False, help_text="Feature this bride on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def get_all_images(self):
        """Get all images including main image and additional images"""
        images = []
        if self.image:
            images.append({
                'url': self.image.url,
                'caption': f"{self.name} - Main Photo",
                'is_main': True
            })
        
        for bride_image in self.additional_images.all():
            images.append({
                'url': bride_image.image.url,
                'caption': bride_image.caption or f"{self.name} - Photo {bride_image.id}",
                'is_main': False
            })
        
        return images
    
    def get_total_images_count(self):
        """Get total count of all images"""
        count = 1 if self.image else 0
        count += self.additional_images.count()
        return count
    
    class Meta:
        ordering = ['-event_date', '-created_at']
        verbose_name = "Bride"
        verbose_name_plural = "My Brides"

class BrideImage(models.Model):
    """Model for additional bride images"""
    bride = models.ForeignKey(Bride, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='brides/additional/', help_text="Additional bride photo")
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for this image")
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bride.name} - Image {self.id}"
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Bride Image"
        verbose_name_plural = "Bride Images"

class Customer(models.Model):
    """Model for customer information"""
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Invoice(models.Model):
    """Model for invoice"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    issue_date = models.DateField()
    due_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    tax_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    advance_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Amount paid in advance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate unique invoice number
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def get_subtotal(self):
        """Calculate subtotal before tax and discount"""
        return sum(item.get_total() for item in self.items.all())
    
    def get_discount_amount(self):
        """Calculate discount amount"""
        return (self.get_subtotal() * self.discount_percentage) / 100
    
    def get_tax_amount(self):
        """Calculate tax amount after discount"""
        amount_after_discount = self.get_subtotal() - self.get_discount_amount()
        return (amount_after_discount * self.tax_percentage) / 100
    
    def get_total(self):
        """Calculate final total"""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return subtotal - discount + tax
    
    def get_due_amount(self):
        """Calculate due amount after advance payment"""
        return max(self.get_total() - self.advance_amount, Decimal('0.00'))
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"
    
    class Meta:
        ordering = ['-created_at']

class InvoiceItem(models.Model):
    """Model for invoice line items"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    def get_total(self):
        """Calculate line item total"""
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.description} x {self.quantity}"
    
    class Meta:
        ordering = ['id']

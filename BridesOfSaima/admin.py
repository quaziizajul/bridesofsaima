from django.contrib import admin
from .models import Customer, Invoice, InvoiceItem, Bride, BrideImage

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('customer__name', 'invoice_number')

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price')
    list_filter = ('invoice__created_at',)

class BrideImageInline(admin.TabularInline):
    model = BrideImage
    extra = 1
    fields = ('image', 'caption', 'order')
    verbose_name = "Additional Image"
    verbose_name_plural = "Additional Images"

@admin.register(Bride)
class BrideAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'event_date', 'get_total_images_count', 'created_at')
    list_filter = ('event_date', 'location', 'created_at', 'is_featured')
    search_fields = ('name', 'location', 'tagline')
    date_hierarchy = 'event_date'
    ordering = ('-event_date',)
    inlines = [BrideImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'event_date', 'tagline')
        }),
        ('Main Image', {
            'fields': ('image',),
            'description': 'This image will be shown as the thumbnail in the gallery'
        }),
        ('Settings', {
            'fields': ('is_featured',),
            'classes': ('collapse',)
        })
    )
    
    def get_total_images_count(self, obj):
        return obj.get_total_images_count()
    get_total_images_count.short_description = 'Total Images'

@admin.register(BrideImage)
class BrideImageAdmin(admin.ModelAdmin):
    list_display = ('bride', 'caption', 'order', 'created_at')
    list_filter = ('created_at', 'bride__location')
    search_fields = ('bride__name', 'caption')
    ordering = ('bride', 'order', 'created_at')

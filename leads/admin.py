from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("company_name", "industry", "email", "employee_count", "estimated_revenue")
    search_fields = ("company_name", "domain", "industry", "email", "location")
    list_filter = ("industry", "source")

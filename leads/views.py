import csv
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import LeadForm
from .models import Lead
from .services import filtered_leads, import_sample_leads, normalize_domain

def dashboard(request):
    leads = filtered_leads(request.GET)
    all_leads = list(Lead.objects.all())
    industries = Lead.objects.exclude(industry="").values_list("industry", flat=True).distinct().order_by("industry")
    context = {
        "leads": leads,
        "total_count": len(all_leads),
        "high_count": sum(1 for lead in all_leads if lead.quality_label == "High"),
        "incomplete_count": sum(1 for lead in all_leads if lead.missing_fields),
        "industry_options": industries,
        "query": request.GET.get("q", ""),
        "selected_industry": request.GET.get("industry", ""),
        "selected_quality": request.GET.get("quality", ""),
    }
    return render(request, "leads/dashboard.html", context)

def add_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.domain = normalize_domain(lead.domain)
            lead.email = lead.email.strip().lower()
            if lead.domain and Lead.objects.filter(domain__iexact=lead.domain).exists():
                form.add_error("domain", "A lead with this domain already exists.")
            elif lead.email and Lead.objects.filter(email__iexact=lead.email).exists():
                form.add_error("email", "A lead with this email already exists.")
            else:
                lead.save()
                messages.success(request, "Lead added successfully.")
                return redirect("leads:dashboard")
    else:
        form = LeadForm()
    return render(request, "leads/lead_form.html", {"form": form, "page_title": "Add a lead"})

def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.domain = normalize_domain(updated.domain)
            updated.email = updated.email.strip().lower()
            if updated.domain and Lead.objects.filter(domain__iexact=updated.domain).exclude(pk=pk).exists():
                form.add_error("domain", "Another lead with this domain already exists.")
            elif updated.email and Lead.objects.filter(email__iexact=updated.email).exclude(pk=pk).exists():
                form.add_error("email", "Another lead with this email already exists.")
            else:
                updated.save()
                messages.success(request, "Lead updated successfully.")
                return redirect("leads:dashboard")
    else:
        form = LeadForm(instance=lead)
    return render(request, "leads/lead_form.html", {"form": form, "page_title": "Edit lead"})

@require_POST
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, "Lead deleted.")
    return redirect("leads:dashboard")

@require_POST
def import_sample(request):
    created, skipped = import_sample_leads()
    messages.success(request, f"Sample import complete: {created} added, {skipped} duplicates skipped.")
    return redirect("leads:dashboard")

def export_csv(request):
    leads = filtered_leads(request.GET)
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="leadlens_leads.csv"'
    response.write("\\ufeff")
    writer = csv.writer(response)
    writer.writerow([
        "Company", "Domain", "Industry", "Employees", "Estimated revenue",
        "Contact", "Email", "Location", "Source", "Quality score", "Quality level", "Missing fields",
    ])
    for lead in leads:
        writer.writerow([
            lead.company_name, lead.domain, lead.industry, lead.employee_count,
            lead.estimated_revenue if lead.estimated_revenue is not None else "",
            lead.contact_name, lead.email, lead.location, lead.source,
            lead.quality_score, lead.quality_label, ", ".join(lead.missing_fields),
        ])
    return response

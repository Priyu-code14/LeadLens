import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from django.db.models import Q
from .models import Lead

def normalize_domain(value):
    value = (value or "").strip().lower()
    value = value.removeprefix("https://").removeprefix("http://")
    value = value.removeprefix("www.").split("/")[0]
    return value

def import_sample_leads():
    """Import the bundled, fictional demonstration dataset without duplicates."""
    path = Path(__file__).resolve().parent.parent / "sample_data" / "sample_leads.csv"
    created = 0
    skipped = 0
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            domain = normalize_domain(row.get("domain"))
            email = (row.get("email") or "").strip().lower()
            qs = Lead.objects.all()
            duplicate = False
            if domain and qs.filter(domain__iexact=domain).exists():
                duplicate = True
            if email and qs.filter(email__iexact=email).exists():
                duplicate = True
            if duplicate:
                skipped += 1
                continue
            revenue_text = (row.get("estimated_revenue") or "").strip()
            try:
                revenue = Decimal(revenue_text) if revenue_text else None
            except InvalidOperation:
                revenue = None
            Lead.objects.create(
                company_name=(row.get("company_name") or "").strip(),
                domain=domain,
                industry=(row.get("industry") or "").strip(),
                employee_count=int(row.get("employee_count") or 0),
                estimated_revenue=revenue,
                contact_name=(row.get("contact_name") or "").strip(),
                email=email,
                location=(row.get("location") or "").strip(),
                source=(row.get("source") or "Sample dataset").strip(),
                notes=(row.get("notes") or "").strip(),
            )
            created += 1
    return created, skipped

def filtered_leads(params):
    qs = Lead.objects.all()
    query = (params.get("q") or "").strip()
    industry = (params.get("industry") or "").strip()
    quality = (params.get("quality") or "").strip().lower()
    if query:
        qs = qs.filter(
            Q(company_name__icontains=query) |
            Q(domain__icontains=query) |
            Q(industry__icontains=query) |
            Q(contact_name__icontains=query) |
            Q(email__icontains=query) |
            Q(location__icontains=query)
        )
    if industry:
        qs = qs.filter(industry__iexact=industry)
    # Quality is a Python-computed heuristic, so filter after retrieving rows.
    leads = list(qs)
    if quality in {"high", "medium", "low"}:
        leads = [lead for lead in leads if lead.quality_label.lower() == quality]
    return leads

# LeadLens — Lead Quality Dashboard

A small Django full-stack demonstration for the Caprae Capital lead-generation pre-work assignment. It focuses on **transparent lead-quality scoring**, **duplicate prevention**, **search/filtering**, and **CSV export**.

> The included dataset is fictional demonstration data. Scores are rule-based completeness heuristics, not AI predictions or guarantees of sales conversion. The app does not scrape third-party websites or connect to paid data providers.

## Features

- Dashboard metrics for total leads, high-quality leads, incomplete records, and filtered results.
- Search by company, domain, industry, contact, email, or location.
- Filter by industry and heuristic quality band.
- Add, edit, and delete records with server-side form validation and CSRF protection.
- Normalize domains and email addresses and prevent duplicate domain/email entries.
- Detect incomplete records and explain which fields are missing.
- Export the current filtered view to CSV.
- Import the bundled fictional sample dataset; repeat imports skip duplicates.
- Responsive Bootstrap interface.

## Tech stack

- Python 3.10+
- Django 5.2
- SQLite for easy local setup
- HTML, CSS, Bootstrap 5.3, and vanilla JavaScript

SQLite was chosen to make the assignment quick to run and reproducible. For a production deployment, configure a managed database using environment variables, add authentication and authorization, move secrets out of source code, and configure HTTPS, logging, backups, rate limits, and monitoring.

## Run locally (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

Click **Load sample data** to import fictional sample records.

If PowerShell blocks virtual environment activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell window, then activate again.

## Optional admin account

```powershell
python manage.py createsuperuser
```

Then visit http://127.0.0.1:8000/admin/

## Quality scoring

| Signal | Points |
|---|---:|
| Company name present | 15 |
| Domain present | 20 |
| Industry present | 15 |
| Employee count greater than zero | 15 |
| Revenue estimate present | 15 |
| Contact name present | 10 |
| Email present | 10 |
| **Maximum** | **100** |

The score measures record completeness only. It does not determine whether a company is financially attractive or likely to become a customer. In a real acquisition-sourcing workflow, scoring rules should be configurable and validated with users.

## Architecture

Browser → Django views/forms → Django ORM → SQLite. Business logic for normalization, sample import, filtering, and deduplication lives in `leads/services.py`; the score and missing-field checks live on the `Lead` model. CSV export is generated on demand from the current filters. No cache is included because this small local demo has a tiny dataset; if it grew, measure query performance first and cache only suitable read-heavy computations with clear invalidation.

## Project structure

```text
LeadLens/
├── config/                 # Django settings and URL configuration
├── leads/
│   ├── migrations/
│   ├── static/leads/       # CSS and JavaScript
│   ├── templates/leads/    # Dashboard and form templates
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── sample_data/sample_leads.csv
├── manage.py
├── requirements.txt
└── README.md
```

## Test checklist

- [ ] Run `python manage.py check`.
- [ ] Run migrations and open the dashboard.
- [ ] Load sample data twice; second import should skip existing domains/emails.
- [ ] Add a lead and try reusing an existing domain or email.
- [ ] Search and filter leads, then export the filtered view.
- [ ] Edit a record and confirm the score changes with its field completeness.
- [ ] Delete a record and confirm it disappears.

## Known limitations

- No live scraping, third-party enrichment, CRM integration, user accounts, or production hosting is implemented.
- Revenue is a user-entered estimate; it is not independently verified.
- SQLite and the development settings are for local demonstration, not production.
- Sample company names, domains, and contacts are fictional. The `.example` domains are reserved examples and are not real business websites.

## Demo video outline (1–2 minutes)

1. **Problem (10–15 sec):** Sales/acquisition teams can waste time on duplicate or incomplete lead records.
2. **Walkthrough (40–50 sec):** Load sample records, show quality scores, filter by industry/quality, inspect missing fields, add/edit a lead, and export CSV.
3. **Technical choices (20–25 sec):** Explain Django, the data model, server-side validation, duplicate prevention, and CSV export.
4. **Impact and next step (10–15 sec):** Explain that a production version could add verified enrichment sources, configurable scoring, and integrations after validation.

Record only features that work in your actual demo.

# Generated for LeadLens demonstration project.
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(max_length=180)),
                ("domain", models.CharField(blank=True, max_length=180)),
                ("industry", models.CharField(blank=True, max_length=100)),
                ("employee_count", models.PositiveIntegerField(default=0)),
                ("estimated_revenue", models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ("contact_name", models.CharField(blank=True, max_length=180)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("location", models.CharField(blank=True, max_length=180)),
                ("source", models.CharField(default="Sample dataset", max_length=100)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["company_name", "id"]},
        ),
    ]

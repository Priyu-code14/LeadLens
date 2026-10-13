from django.db import models

class Lead(models.Model):
    company_name = models.CharField(max_length=180)
    domain = models.CharField(max_length=180, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.PositiveIntegerField(default=0)
    estimated_revenue = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    contact_name = models.CharField(max_length=180, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=180, blank=True)
    source = models.CharField(max_length=100, default="Sample dataset")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["company_name", "id"]

    def __str__(self):
        return self.company_name

    @property
    def quality_score(self):
        """Transparent heuristic score (0–100), not an AI prediction."""
        score = 0
        if self.company_name.strip():
            score += 15
        if self.domain.strip():
            score += 20
        if self.industry.strip():
            score += 15
        if self.employee_count > 0:
            score += 15
        if self.estimated_revenue is not None:
            score += 15
        if self.contact_name.strip():
            score += 10
        if self.email.strip():
            score += 10
        return min(score, 100)

    @property
    def quality_label(self):
        if self.quality_score >= 80:
            return "High"
        if self.quality_score >= 50:
            return "Medium"
        return "Low"

    @property
    def missing_fields(self):
        fields = []
        if not self.domain:
            fields.append("domain")
        if not self.industry:
            fields.append("industry")
        if not self.contact_name:
            fields.append("contact")
        if not self.email:
            fields.append("email")
        if not self.employee_count:
            fields.append("employee count")
        return fields

from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("leads/add/", views.add_lead, name="add_lead"),
    path("leads/<int:pk>/edit/", views.edit_lead, name="edit_lead"),
    path("leads/<int:pk>/delete/", views.delete_lead, name="delete_lead"),
    path("import-sample/", views.import_sample, name="import_sample"),
    path("export.csv", views.export_csv, name="export_csv"),
]

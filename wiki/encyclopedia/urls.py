from django.urls import path
from . import views
app_name = 'note'

urlpatterns = [
    path("", views.index, name="index"),
    path("createnewpage", views.create, name="createnewpage"),
    path("deletepage", views.delete, name="deletepage"),
    path("editpage", views.edit, name="editpage"),
    path("randompage", views.randompick, name="randompage"),
    path("<str:title>", views.entry, name = "entry")
]

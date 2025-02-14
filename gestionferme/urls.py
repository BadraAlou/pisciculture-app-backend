# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('pdf/pisciculture/<int:cycle_id>/', views.generate_pisciculture_pdf, name='pisciculture_pdf'),
    path('export_all_cycles_to_pdf/', views.export_all_cycles_to_pdf, name='export_all_cycles_to_pdf'),

    # autres routes
]

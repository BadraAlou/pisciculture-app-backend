# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import CycleProduction  # ou le modèle que vous utilisez pour la pisciculture
from weasyprint import HTML
from django.template.loader import render_to_string

def generate_pisciculture_pdf(request, cycle_id):
    # Récupérez les données du cycle de production
    cycle = CycleProduction.objects.get(id=cycle_id)
    infrastructures = cycle.infrastructure_set.all()
    
    # Créez le contexte pour le template
    context = {
        'cycle': cycle,
        'infrastructures': infrastructures,
    }

    # Générez le HTML à partir du template
    html_string = render_to_string('pisciculture_template.html', context)
    html = HTML(string=html_string)

    # Créez une réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Pisciculture_{cycle.nom}.pdf"'
    html.write_pdf(response)

    return response


def export_all_cycles_to_pdf(request):
    # Récupérer tous les cycles de production
    cycles = CycleProduction.objects.all()

    # Rendre le template HTML pour le PDF
    html_string = render_to_string('gestionferme/cycle_production_list_pdf.html', {'cycles': cycles})
    
    # Convertir en PDF avec WeasyPrint
    html = HTML(string=html_string)
    pdf_content = html.write_pdf()

    # Retourner la réponse en PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cycles_production.pdf"'
    return response



from django.contrib.admin.views.decorators import staff_member_required
#from django.shortcuts import render

@staff_member_required
def custom_dashboard(request):
    # Exemple de données pour le tableau de bord
    stats = {
        "total_users": 100,
        "total_orders": 50,
        "pending_tasks": 10,
    }
    return render(request, 'gestionferme/admin/custom_dashboard.html', {'stats': stats})
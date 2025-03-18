from pyexpat.errors import messages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from unfold.decorators import action  # Import @action decorator from Unfold



from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import (
    TextFilter, FieldTextFilter, RelatedDropdownFilter, RangeDateFilter, 
    RangeNumericListFilter, RangeNumericFilter, SingleNumericFilter, SliderNumericFilter,
    DropdownFilter, ChoicesDropdownFilter
)

from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget


# Register your models here.
from .models import *

admin.site.unregister(User)
admin.site.unregister(Group)






class RationJournaliereTabularInline(TabularInline):
    model = RationJournaliere
    show_change_link = True
    #list_display = ["date", "etudiant", "evaluation"]
    extra = 0 
    #tab = True
    # fieldsets = (

    #     (
    #          _("Répartion entre types aliments"),
    #               {
    #                   "classes": ["tab"],
    #                   "fields": [
    #                       "aliment1", "aliment2", "aliment3", "aliment4", "aliment5"
    #                   ],
    #               },
    #     ),

    #     (
    #          _("Traitements sanitaires"),
    #               {
    #                   "classes": ["tab"],
    #                   "fields": [
    #                       "produit1", "produit2"
    #                   ],
    #               },
    #     ),
    # )

class PecheControleTabularInline(TabularInline):
    model = PecheControle
    show_change_link = True
    extra = 0
    #tab = True
    #fieldsets = [('Info 1', {'fields': ['date',], 'classes':['collapse']}), ('Info 2', {'fields': ['nombreEchantillons', 'nombreTotalPoissonsEchantillonnes', 'poidsTotalEchantillons'], 'classes': ['collapse']}),]
    
    

class AlevinTabularInline(TabularInline):
    model = Alevin
    show_change_link = True
    #per_page = 1
    extra = 0
    #tab = True


class RecolteTabularInline(TabularInline):
    model = Recolte
    show_change_link = True
    extra = 0
    #tab = True

class InfrastructureTabularInline(TabularInline):
    model = Infrastructure
    show_change_link = True
    extra = 0
    #tab = True


class CycleProductionTabularInline(TabularInline):
    model = CycleProduction
    show_change_link = True
    extra = 0


class FermeTabularInline(TabularInline):
    model = Ferme
    show_change_link = True
    extra = 0
    #tab = True


class ChargeTabularInline(TabularInline):
    model = Charge
    show_change_link = True
    extra = 0




@admin.register(Pisciculteur)
class PisciculteurAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter_submit = True
    # Display changelist in fullwidth
    #list_fullwidth = False
    inlines = [FermeTabularInline ]
    actions = []

    warn_unsaved_form = True 
    list_display = ['matricule', 'nom', 'prenom', 'genre', 'telephone', 'adresse', 'email']
    list_filter = [('matricule', FieldTextFilter), ('nom', FieldTextFilter), ('prenom', FieldTextFilter)]
                #    ('etudiant', RelatedDropdownFilter), ('etudiant__genre', ChoicesDropdownFilter), ('evaluation', FieldTextFilter),
                #    ('python', RangeNumericFilter), ('oracle', RangeNumericFilter,), ('java', RangeNumericFilter), 
                #     ('ccna', RangeNumericFilter) ]
    search_fields = ('nom', 'prenom' ,'matricule', 'email', 'telephone')



@admin.register(Zone)
class ZoneAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True
    list_fullwidth = True
    warn_unsaved_form = True 
    list_display = ['nom', 'pays', 'region', 'cercle', 'commune', 'ville', 'quartier']
    list_filter = [('nom', FieldTextFilter), ('ville', FieldTextFilter), ('quartier', FieldTextFilter)]   
    search_fields = ('nom', 'pays',  'region',  'cercle',  'commune', 'ville', 'quartier')


@admin.register(Ferme)
class FermeAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [CycleProductionTabularInline, ]
    #list_fullwidth = True
    warn_unsaved_form  = True 
    list_display  = ['nom', 'zone', 'pisciculteur']
    list_filter  = [('nom', FieldTextFilter), ('zone__nom', FieldTextFilter)]
    search_fields  =  ('nom', 'zone__nom', 'pisciculteur__nom', 'pisciculteur__prenom')


@admin.register(TypeInfrastructure)
class TypeInfrastructureAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    #list_fullwidth = True 
    warn_unsaved_form   = True 
    list_display   = ['nom']
    search_fields   = ('nom',)


@admin.register(Infrastructure)
class InfrastructureAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    #list_fullwidth = True 
    warn_unsaved_form   = True 
    #inlines = [CycleProductionTabularInline ]
    list_display   = ['typeInfrastructure', 'numero', 'superficie', 'volume',
                    'dateConstruction', 'dateReabilitation', 'natureReabilitation']
    search_fields   = ('numero', 'typeInfrastructure__nom')

    fieldsets = (

        (
             _("Infos Generale"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "typeInfrastructure"
                      ],
                  },
        ),

        (
             _("Infrastructure"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        "numero", "superficie", "volume", "dateConstruction"
                      ],
                  },
        ),

        (
             _("Réhabilitation"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "dateReabilitation", "natureReabilitation"
                      ],
                  },
        ),
    )






@admin.register(CycleProduction)
class CycleProductionAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [InfrastructureTabularInline ,AlevinTabularInline, RationJournaliereTabularInline,
                PecheControleTabularInline, RecolteTabularInline, ChargeTabularInline ]
    
    #list_fullwidth = True 
    warn_unsaved_form    = True 
    list_display   = ['nom', 'ferme','cycle', 'pdf_rapport_infrastructure', 'pdf_bilan_financier']
    search_fields   = ('nom',)

    def pdf_rapport_infrastructure(self, obj):
        url = reverse('admin:cycleproduction_infrastructure_pdf', args=[obj.id])
        return format_html('<a href="{}">Télecharger</a>', url)

    pdf_rapport_infrastructure.short_description = "Rapport Infrast."

    def pdf_bilan_financier(self, obj):
        url = reverse('admin:cycleproduction_bilan_financier_pdf', args=[obj.id])
        return format_html('<a href="{}">Télecharger</a>', url)

    pdf_bilan_financier.short_description = "Bilan Financier"

    # Ajout de l'URL pour la génération du PDF dans l'admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:cycle_id>/bilan_infrastrucre/', self.admin_site.admin_view(self.generate_bilan_infras_pdf), name='cycleproduction_infrastructure_pdf'),
            path('<int:cycle_id>/bilan_financier/', self.admin_site.admin_view(self.rapport_financier_ferme_pdf), name='cycleproduction_bilan_financier_pdf'),
        ]
        return custom_urls + urls
    


    # Vue qui génère le PDF
    def generate_bilan_infras_pdf(self, request, cycle_id):
        cycle = CycleProduction.objects.get(pk=cycle_id)
        infrastructures = cycle.infrastructure_set.all()
        alevins = Alevin.objects.filter(cycleProduction__id=cycle_id)
        rationJournalieres = RationJournaliere.objects.filter(cycleProduction__id=cycle_id)
        pecheControles = PecheControle.objects.filter(cycleProduction__id=cycle_id)
        recoltes = Recolte.objects.filter(cycleProduction__id=cycle_id)
        charges = Charge.objects.filter(cycleProduction__id=cycle_id)
        
        context = {
            'cycle': cycle,
            #'infrastructures': infrastructures,
            'infrastructures': infrastructures[0],
            'alevin': alevins[0],
            'rationJournaliere': rationJournalieres[0],
            'pecheControle': pecheControles[0],
            'recolte': recoltes[0],
            'charge': charges[0],
        }
        #html_string = render_to_string('gestionferme/pisciculture_template.html', context)
        html_string = render_to_string('gestionferme/bilan_cycle_pisciculteur.html', context)
        html = HTML(string=html_string)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Pisciculture_{cycle.nom}.pdf"'
        html.write_pdf(response)
        return response
    
    def rapport_financier_ferme_pdf(self, request, cycle_id):
        cycle = CycleProduction.objects.get(pk=cycle_id)
        infrastructures = cycle.infrastructure_set.all()
        charges = Charge.objects.filter(cycleProduction__id=cycle_id)
        #print("*** Yo charge : ", charges[0].eau)
        

        totalAlevin = cycle.get_production_summary()
        totalRation = cycle.get_ration_journaliere_summary()
        totalRecolte = cycle.get_recolte_summary()
        #print(f'Yo total ration : {totalRation}')
        #print(f'Yo total recolte : {totalRecolte}')
        
        totalAlevin.calculer_totaux()
        totalRation.calculer_totaux()
        totalRecolte.calculer_totaux()
        # print(f"Yo Recette - nbre Tilapia : {totalRecolte['data']['vente']['tilapia']['bassin_en_ciment']}")
        print(f"Yo Recette - nbre Tilapia : {totalRecolte.data['vente']['tilapia']['bassin_en_ciment']}")
        print(f"Yo Recette - nbre Tilapia : {totalRecolte.data['vente']['couts']['tilapia']['bassin_en_ciment']}")
        totalCharge = totalAlevin.cout_total + totalRation.cout_total + totalRation.cout_total_prod + charges[0].coutTotalCharges()
        

        context = {
            'cycle': cycle,
            #'infrastructures': infrastructures,
            'infrastructures': infrastructures[0],
            'totalAlevin': totalAlevin,
            'totalRation': totalRation,
            'totalRecolte': totalRecolte,
            #'charges': charges[0],
            'autresCharges': intcomma(charges[0].coutTotalCharges()),
            'totalCharges': intcomma(totalCharge)
        }
        #html_string = render_to_string('gestionferme/pisciculture_template.html', context)
        html_string = render_to_string('gestionferme/rapport_financier_ferme.html', context)
        html = HTML(string=html_string)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Rapport_Financier_Ferme_{cycle.nom}.pdf"'
        html.write_pdf(response)
        return response
    
    @action(description="export_selected_cycles_to_pdf")
    def export_selected_cycles_to_pdf(self, request, queryset):
            # Vérifier si une sélection a été faite, sinon utiliser tous les objets
            if queryset.exists():
                cycles = queryset
                message = "Les cycles sélectionnés ont été exportés en PDF."
            else:
                cycles = CycleProduction.objects.all()
                message = "Tous les cycles ont été exportés en PDF, car aucune sélection n'a été faite."

            # Rendre le template HTML pour le PDF
            html_string = render_to_string('gestionferme/cycle_production_list_pdf.html', {'cycles': cycles})
            
            # Générer le PDF
            html = HTML(string=html_string)
            pdf_content = html.write_pdf()

            # Retourner la réponse PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="cycles_production.pdf"'
            response['Content-Disposition'] = f'inline; filename="cycles_production.pdf"'

            # Ajouter un message de succès dans l'interface d'administration
            #self.message_user(request, message, messages.SUCCESS)
            return response

    export_selected_cycles_to_pdf.short_description = "Exporter en PDF les cycles sélectionnés"
    
    actions = ['export_selected_cycles_to_pdf']


@admin.register(PecheControle)
class PecheControleAdminClass(ImportExportModelAdmin, ModelAdmin):
    mport_form_class = ImportForm
    export_form_class = ExportForm
    #list_fullwidth = True 
    warn_unsaved_form     = True 
    list_display    = ['date', 'nombreEchantillons', 'nombreTotalPoissonsEchantillonnes',
            'poidsTotalEchantillons', 'poidsMoyen', 'prisePoidsTotal', 'biomasse']
    search_fields    = ('date',)

    


@admin.register(RationJournaliere)
class RationJournaliereAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    #list_fullwidth = True 
    warn_unsaved_form      = True 
    #list_display    = ['nom', 'aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5']
    list_display    = ['aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5']
    #search_fields     = ('nom',)

    fieldsets = (

        (
             _("Répartion entre types aliments"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          ("aliment1", "prixAliment1"), ("aliment2", "prixAliment2"),
                          ("aliment3", "prixAliment3"), ("aliment4", "prixAliment4"),
                          ("aliment5", "prixAliment5")
                      ],
                  },
        ),

        (
             _("Traitements sanitaires"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          ("produit1", "prixProduit1"), ("produit2", "prixProduit2"),
                          ("produit3", "prixProduit3")
                      ],
                  },
        ),
    )



@admin.register(Alevin)
class AlevinAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
     #list_fullwidth = True 
    warn_unsaved_form    = True 
    list_display   = ['cycleProduction', 'nombreTilapia', 'nombreClaria',  'nombreAutres',]
    search_fields   = ('ferme__nom',)

    fieldsets = (

        (
             _("Cycle"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "cycleProduction",
                          "infrastructure"
                      ],
                  },
         ),
        
        (
            _("Nombre Alevins"),
            {
                "classes": ["tab"],
                "fields": [
                    "nombreTilapia",
                    "nombreClaria",
                    "nombreAutres",
                ],
            },
        ),

        (
            _("Coût d'Achat des alevins"),
            {
                "classes": ["tab"],
                "fields": [
                    "coutAchatTilapia",
                    "coutAchatClaria",
                    "coutAchatAutres",
                ],
            },
        ),

        (
            _("Mortalité"),
             {
                 "classes": ["tab"],
                 "fields": [
                     "mortaliteTilapia",
                     "mortaliteClaria",
                     "mortaliteAutres",
                 ],
             },
         ),

         
         (
             _("Remplace Mortalite"),
               {
                   "classes": ["tab"],
                   "fields": [
                       "remplaceMortaliteTilapia",
                       "remplaceMortaliteClaria",
                       "remplaceMortaliteAutres",
                   ],
               },
         ),

         (
             _("Biomasse (en kg)"),
                 {
                     "classes": ["tab"],
                     "fields": [
                         "biomasseTilapia",
                         "biomasseClaria",
                         "biomasseAutres",
                     ],
                 },

         ),

         (
             _("Poids moyen (en g)") ,
                  {
                      "classes": ["tab"],
                      "fields":[
                          "poidsMoyenTilapia",
                          "poidsMoyenClaria",
                          "poidsMoyenAutres",
                      ],
                  },
         ),
        
    )




@admin.register(Recolte)
class RecolteAdmin(ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
     #list_fullwidth = True 
    warn_unsaved_form    = True 
    list_display   = ['dateVenteTilapia', 'poidsTotalVenteTilapia', 'recetteTilapia',  ]
    search_fields   = ('dateVenteTilapia',)

    fieldsets = (

        (
             _("Tilapia"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "dateVenteTilapia", "poidsTotalVenteTilapia", "recetteTilapia",
                          "dateDonTilapia", "poidsTotalDonTilapia",
                          "dateAutoConsommationTilapia", "poidsTotalAutoConsommationTilapia"
                      ],
                  },
        ),

        (
            _("Clarias"),
            {
                "classes":  ["tab"],
                "fields":[
                    "dateVenteClarias", "poidsTotalVenteClarias", "recetteClarias",
                    "dateDonClarias", "poidsTotalDonClarias",
                    "dateAutoConsommationClarias", "poidsTotalAutoConsommationClarias"
                ],
            }
        ),

        (
            _("Autres"),
            {
                "classes":   ["tab"],
                "fields":[
                    "dateVenteAutres",  "poidsTotalVenteAutres",  "recetteAutres",
                    "dateDonAutres",  "poidsTotalDonAutres",
                    "dateAutoConsommationAutres",  "poidsTotalAutoConsommationAutres"
                ],
            }
        )

        
    )



@admin.register(Aliment)
class AlimentAdminClass(ImportExportModelAdmin, ModelAdmin):
    warn_unsaved_form      = True 
    list_display    = ['nom', 'quantite', 'prix']

@admin.register(Produit)
class ProduitAdminClass(ImportExportModelAdmin, ModelAdmin):
    list_display    = ['nom', 'quantite', 'prix']

    



@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass



# admin.py
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import CycleProduction
from django.utils.html import format_html
from django.urls import reverse

def export_cycles_to_pdf(modeladmin, request, queryset):
    # Récupérer tous les cycles de production sélectionnés
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

export_cycles_to_pdf.short_description = "Exporter tous les cycles de production en PDF"




#@admin.register(CycleProduction)
class CycleProductionAdmin2(admin.ModelAdmin):
    list_display = ['date', 'nom', 'ferme', 'pdf_link']
    search_fields = ('nom',)

    # Ajouter l'action de génération de PDF
    #actions = [export_cycles_to_pdf]

    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['custom_button'] = True  # Ajouter un indicateur pour afficher le bouton
    #     return super().changelist_view(request, extra_context=extra_context)

    # def custom_export_pdf_button(self):
    #     url = reverse('export_all_cycles_to_pdf')
    #     return format_html('<a class="button" href="{}">Exporter tous les cycles en PDF</a>', url)

    # custom_export_pdf_button.short_description = "Exporter PDF"

    # Ajouter custom_export_pdf_button dans les actions affichées
    #change_list_template = "gestionferme/cycleproduction_change_list.html"
    
    # Ajout du lien vers le PDF dans l'interface admin
    def pdf_link(self, obj):
        url = reverse('admin:cycleproduction_cycleproduction_pdf', args=[obj.id])
        return format_html('<a href="{}">Télécharger le PDF</a>', url)

    pdf_link.short_description = "Générer PDF"



     # Ajout de l'action
    
    @action(description="export_selected_cycles_to_pdf")
    def export_selected_cycles_to_pdf(self, request, queryset):
            # Vérifier si une sélection a été faite, sinon utiliser tous les objets
            if queryset.exists():
                cycles = queryset
                message = "Les cycles sélectionnés ont été exportés en PDF."
            else:
                cycles = CycleProduction.objects.all()
                message = "Tous les cycles ont été exportés en PDF, car aucune sélection n'a été faite."

            # Rendre le template HTML pour le PDF
            html_string = render_to_string('gestionferme/cycle_production_list_pdf.html', {'cycles': cycles})
            
            # Générer le PDF
            html = HTML(string=html_string)
            pdf_content = html.write_pdf()

            # Retourner la réponse PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="cycles_production.pdf"'

            # Ajouter un message de succès dans l'interface d'administration
            self.message_user(request, message, messages.SUCCESS)
            
            return response

    export_selected_cycles_to_pdf.short_description = "Exporter en PDF les cycles sélectionnés"


    
    actions = ['export_selected_cycles_to_pdf']



    # Ajout de l'URL pour la génération du PDF dans l'admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:cycle_id>/pdf/', self.admin_site.admin_view(self.generate_pdf), name='cycleproduction_cycleproduction_pdf'),
        ]
        return custom_urls + urls

    # Vue qui génère le PDF
    def generate_pdf(self, request, cycle_id):
        cycle = CycleProduction.objects.get(pk=cycle_id)
        infrastructures = cycle.infrastructure_set.all()
        context = {
            'cycle': cycle,
            'infrastructures': infrastructures,
        }
        html_string = render_to_string('gestionferme/pisciculture_template.html', context)
        html = HTML(string=html_string)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Pisciculture_{cycle.nom}.pdf"'
        html.write_pdf(response)
        return response
    



from django.views.generic import TemplateView
from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin

# @admin.register(Dashboard)
# class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
#     title = "Custom Title"  # required: custom page header title
#     permission_required = () # required: tuple of permissions
#     template_name = "gestionferme/custom_page.html"


# @admin.register(Dashboard)
# class CustomAdmin(ModelAdmin):
#     def get_urls(self):
#         return super().get_urls() + [
#             path(
#                 "custom-url-path",
#                 MyClassBasedView.as_view(model_admin=self),  # IMPORTANT: model_admin is required
#                 name="custom_name"
#             ), 
#         ]
    

# from django.urls import reverse
# from django.utils.html import format_html

# class CustomAdminSite(admin.AdminSite):
#     site_header = "Administration personnalisée"
#     site_title = "Tableau de bord"
#     index_title = "Bienvenue dans l'administration"

#     def index(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['dashboard_url'] = reverse('custom_dashboard')
#         return super().index(request, extra_context=extra_context)

# admin_site = CustomAdminSite(name='custom_admin')
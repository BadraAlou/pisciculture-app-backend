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
from .forms import CustomUserCreationForm, CustomUserChangeForm
import nested_admin

# Register your models here.
from .models import *

#admin.site.unregister(User)
admin.site.unregister(Group)

 


# class CustomUserAdmin(BaseUserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser

#     # Champs affichés dans la liste des utilisateurs
#     list_display = ('email', 'telephone', 'is_staff', 'is_active',)
#     #list_filter = ('is_staff', 'is_active', 'user_type')
#     list_filter = ('is_staff', 'is_active', )

#     # Champs à utiliser dans les formulaires d'ajout
#     add_fieldsets = (
#         # (None, {
#         #     'classes': ('wide',),
#         #     'fields': ('email', 'telephone', 'password1', 'password2', 'is_staff', 'is_active')}
#         # ),

#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'telephone', 'password', 'password2')
#             }),
#         #(_('Informations'), {'fields': ('email', 'telephone', 'password', )}),
#         #(_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Permissions'), {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        
#     )

#     # Champs à utiliser dans les formulaires de modification
#     fieldsets = (
#         (None, {'fields': ('email', 'telephone', 'password')}),
#         (_('Permissions'), {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', )}),
#     )

#     search_fields = ('email', 'telephone')
#     ordering = ('email',)


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'telephone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'telephone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    # ❗ C'est ici que l'admin attendait un champ username : on le remplace
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'telephone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'telephone')
    ordering = ('email',)



#admin.site.unregister(CustomUser)
#admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Pisciculteur)




class QuartierInline(TabularInline):
    model = Quartier
    extra = 1
    show_change_link = True

class VilleInline(TabularInline):
    model = Ville
    extra = 1
    show_change_link = True
    inlines = [QuartierInline]

class CommuneInline(TabularInline):
    model = Commune
    extra = 1
    show_change_link = True
    inlines = [VilleInline]

class CercleInline(TabularInline):
    model = Cercle
    extra = 1
    show_change_link = True
    inlines = [CommuneInline]



class RegionInline(TabularInline):
    model = Region
    extra = 1
    show_change_link = True
    inlines = [CercleInline]



class ChefSecteurCercleInline(TabularInline):
    model = ChefSecteurCercle
    extra = 1


class AffectationRegionInline(admin.TabularInline):
    model = AffectationRegionDirecteur
    extra = 1





class PisciculteurInline(TabularInline):
    model = Pisciculteur
    extra = 0
    #show_change_link = True
    readonly_fields = ('user', 'quartier')
    fields = ['matricule', 'nom', 'prenom', 'quartier', ]
    can_delete = False


# class Ration1TabularInline(TabularInline):
#     model = Ration1
#     show_change_link = True
#     #list_display = ["date", "etudiant", "evaluation"]
#     extra = 0 
#     tab = True

# class Ration2TabularInline(TabularInline):
#     model = Ration2
#     show_change_link = True
#     #list_display = ["date", "etudiant", "evaluation"]
#     extra = 0 
#     tab = True
    

# class CyclesRationTabularInline(TabularInline):
#     model = CyclesRation
#     show_change_link = True
#     #inlines = [Ration1TabularInline, Ration2TabularInline]
#     #list_display = ["date", "etudiant", "evaluation"]
#     extra = 0 
#     tab = True



class RationJournaliereTabularInline(TabularInline):
    model = RationJournaliere
    show_change_link = True
    #list_display = ["date", "etudiant", "evaluation"]
    extra = 0 
    tab = True
    readonly_fields = ('quantite_ration_cycle1',)
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
    readonly_fields = ('poids_total_echant', 'poids_moyen', 'prise_poids_total', 'biomasse_2',
         'date_de_controle_2', 'nombre_echantilons_2', 'nbre_total_poisson_echant_2', 'poids_total_echant_2', 'poids_moyen_2', 'prise_poids_total_2', 'biomasse_3',
         'date_de_controle_3', 'nombre_echantilons_3', 'nbre_total_poisson_echant_3', 'poids_total_echant_3', 'poids_moyen_3', 'prise_poids_total_3', 'biomasse_4',
         'date_de_controle_4', 'nombre_echantilons_4', 'nbre_total_poisson_echant_4', 'poids_total_echant_4', 'poids_moyen_4', 'prise_poids_total_4', 'biomasse_5',
         'date_de_controle_5', 'nombre_echantilons_5', 'nbre_total_poisson_echant_5', 'poids_total_echant_5', 'poids_moyen_5', 'prise_poids_total_5', 'biomasse_6',
         'date_de_controle_6', 'nombre_echantilons_6', 'nbre_total_poisson_echant_6', 'poids_total_echant_6', 'poids_moyen_6', 'prise_poids_total_6', 'biomasse_7',
         )
    tab = True
    #fieldsets = [('Info 1', {'fields': ['date',], 'classes':['collapse']}), ('Info 2', {'fields': ['prise_poids_tilapia', 'prise_poids_claria'], 'classes': ['collapse']}),]
    
    

class AlevinTabularInline(TabularInline):
    model = Alevin
    show_change_link = True
    #per_page = 1
    extra = 0
    tab = True
    readonly_fields = ('biomasse_tilapia', 'biomasse_claria', 'biomasse_autres')
    


class RecolteTabularInline(TabularInline):
    model = Recolte
    show_change_link = True
    extra = 0
    tab = True

class InfrastructureTabularInline(TabularInline):
    model = Infrastructure
    show_change_link = True
    extra = 0
    tab = True


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
    tab = True


from .ressources import *

@admin.register(Pisciculteur)
class PisciculteurAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_class = PisciculteurResource

    list_filter_submit = True
    # Display changelist in fullwidth
    #list_fullwidth = False
    inlines = [FermeTabularInline ]
    actions = []

    warn_unsaved_form = True 
    list_display = ['matricule', 'nom', 'prenom', 'genre', 'quartier']
    #list_filter = [('matricule', FieldTextFilter), ('nom', FieldTextFilter), ('prenom', FieldTextFilter), 
    list_filter = [ 
    ('quartier', RelatedDropdownFilter), ('quartier__ville', RelatedDropdownFilter), ('quartier__ville__commune', RelatedDropdownFilter),
    ('quartier__ville__commune__cercle', RelatedDropdownFilter), ('quartier__ville__commune__cercle__region', RelatedDropdownFilter),
    ('quartier__ville__commune__cercle__region__pays', RelatedDropdownFilter)]
                #    ('etudiant', RelatedDropdownFilter), ('etudiant__genre', ChoicesDropdownFilter), ('evaluation', FieldTextFilter),
                #    ('python', RangeNumericFilter), ('oracle', RangeNumericFilter,), ('java', RangeNumericFilter), 
                #     ('ccna', RangeNumericFilter) ]
    search_fields = ('nom', 'prenom' ,'matricule')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Agent d'encadrement
        try:
            agent = request.user.agent_encadrement_profile
            return qs.filter(agent_encadrement=agent)
        except AgentEncadrement.DoesNotExist:
            pass

        # Chef secteur
        try:
            chef = request.user.chef_secteur_profile
            cercles = chef.cercles.all()
            print(f'Yo les cercles : {cercles}')
            print(qs.filter(
                quartier__ville__commune__cercle__in=cercles
            ))

            return qs.filter(
                quartier__ville__commune__cercle__in=cercles
            )
            

        except ChefSecteur.DoesNotExist:
            return qs.none()


        # Ajoute des boutons dans la barre d'action
    actions = ['export_raw', 'export_readable']

    def export_raw(self, request, queryset):
        resource = PisciculteurRawResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="pisciculteurs_raw.xlsx"'
        return response
    export_raw.short_description = "Exporter (brut - ID)"

    def export_readable(self, request, queryset):
        resource = PisciculteurReadableResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="pisciculteurs_lisible.xlsx"'
        return response
    export_readable.short_description = "Exporter (lisible - noms)"



class ControlleurAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter_submit = True
 
    warn_unsaved_form = True 
    list_display = ['nom', 'prenom', 'adresse']


# @admin.register(Zone)
# class ZoneAdminClass(ImportExportModelAdmin, ModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#     list_filter_submit = True
#     list_fullwidth = True
#     warn_unsaved_form = True 
#     list_display = ['nom', 'pays', 'region', 'cercle', 'commune', 'ville', 'quartier']
#     list_filter = [('nom', FieldTextFilter), ('ville', FieldTextFilter), ('quartier', FieldTextFilter)]   
#     search_fields = ('nom', 'pays',  'region',  'cercle',  'commune', 'ville', 'quartier')


@admin.register(Ferme)
class FermeAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [CycleProductionTabularInline, ]
    #list_fullwidth = True
    warn_unsaved_form  = True 
    list_display  = ['nom', 'quartier', 'pisciculteur']
    list_filter  = [('nom', FieldTextFilter), ('quartier__nom', FieldTextFilter)]
    search_fields  =  ('nom', 'quartier__nom', 'pisciculteur__nom', 'pisciculteur__prenom')

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
    inlines = [InfrastructureTabularInline ,AlevinTabularInline,
                RationJournaliereTabularInline,
                PecheControleTabularInline, RecolteTabularInline, ChargeTabularInline ]
    
    #list_fullwidth = True 
    warn_unsaved_form    = True 
    list_display   = ['nom', 'ferme','cycle', 'pdf_rapport_infrastructure', 'pdf_bilan_financier']
    search_fields   = ('nom',)
    


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Admin voit tout
        if request.user.is_superuser:
            return qs

        # Si l'utilisateur est un pisciculteur
        try:
            pisciculteur = request.user.pisciculteur_profile
            return qs.filter(ferme__pisciculteur=pisciculteur)
        except Pisciculteur.DoesNotExist:
            pass

        # Si l'utilisateur est un agent d'encadrement
        try:
            agent = request.user.agent_encadrement_profile
            return qs.filter(ferme__pisciculteur__agent_encadrement=agent)
        except AgentEncadrement.DoesNotExist:
            pass

        # Sinon, aucun accès
        return qs.none()

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

        try:
            montant_charges = charges[0].coutTotalCharges()
        except:
            montant_charges = 0
        #totalCharge = totalAlevin.cout_total + totalRation.cout_total + totalRation.cout_total_prod + charges[0].coutTotalCharges()
        totalCharge = totalAlevin.cout_total + totalRation.cout_total + totalRation.cout_total_prod + montant_charges
        

        context = {
            'cycle': cycle,
            #'infrastructures': infrastructures,
            'infrastructures': infrastructures[0],
            'totalAlevin': totalAlevin,
            'totalRation': totalRation,
            'totalRecolte': totalRecolte,
            #'charges': charges[0],
            #'autresCharges': intcomma(charges[0].coutTotalCharges()),
            'autresCharges': intcomma(montant_charges),
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
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    #list_fullwidth = True 
    warn_unsaved_form = True
    list_display    = ['date', 'nombreEchantillons', 'nombreTotalPoissonsEchantillonnes', ]
    readonly_fields = ('date_de_controle', 'nombre_echantilons', 'nbre_total_poisson_echant', 'poids_total_echant', 'poids_moyen', 'prise_poids_total', 'biomasse_2',
         'date_de_controle_2', 'nombre_echantilons_2', 'nbre_total_poisson_echant_2', 'poids_total_echant_2', 'poids_moyen_2', 'prise_poids_total_2', 'biomasse_3',
         'date_de_controle_3', 'nombre_echantilons_3', 'nbre_total_poisson_echant_3', 'poids_total_echant_3', 'poids_moyen_3', 'prise_poids_total_3', 'biomasse_4',
         'date_de_controle_4', 'nombre_echantilons_4', 'nbre_total_poisson_echant_4', 'poids_total_echant_4', 'poids_moyen_4', 'prise_poids_total_4', 'biomasse_5',
         'date_de_controle_5', 'nombre_echantilons_5', 'nbre_total_poisson_echant_5', 'poids_total_echant_5', 'poids_moyen_5', 'prise_poids_total_5', 'biomasse_6',
         'date_de_controle_6', 'nombre_echantilons_6', 'nbre_total_poisson_echant_6', 'poids_total_echant_6', 'poids_moyen_6', 'prise_poids_total_6', 'biomasse_7',
         )

    fieldsets = (
        (
            _("Pêche de Controle"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date", "prise_poids_tilapia"), ("prise_poids_claria", "prise_poids_autres"),  ("nombreEchantillons", "nombreTotalPoissonsEchantillonnes"),
                ],
            },
        ),
        (
            _("Cycles 1"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle", "nombre_echantilons", "nbre_total_poisson_echant", "poids_total_echant", "poids_moyen", "prise_poids_total", "biomasse_2"),
                ],
            },
        ),
        (
            _("Pêche de Controle 2"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle_2", "nombre_echantilons_2"), ("nbre_total_poisson_echant_2", "poids_total_echant_2"), ("poids_moyen_2", "prise_poids_total_2"), ("biomasse_3"),
                ],
            },
        ),
        (
            _("Pêche de Controle 3"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle_3", "nombre_echantilons_3"), ("nbre_total_poisson_echant_3", "poids_total_echant_3"), ("poids_moyen_3", "prise_poids_total_3"), ("biomasse_4"),
                ],
            },
        ),
        (
            _("Pêche de Controle 4"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle_4", "nombre_echantilons_4"), ("nbre_total_poisson_echant_4", "poids_total_echant_4"), ("poids_moyen_4", "prise_poids_total_4"), ("biomasse_5"),
                ],
            },
        ),
        (
            _("Pêche de Controle 5"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle_5", "nombre_echantilons_5"), ("nbre_total_poisson_echant_5", "poids_total_echant_5"), ("poids_moyen_5", "prise_poids_total_5"), ("biomasse_6"),
                ],
            },
        ),
        (
            _("Pêche de Controle 6"),
            {
                "classes": ["tab"],
                "fields": [
                    ("date_de_controle_6", "nombre_echantilons_6"), ("nbre_total_poisson_echant_6", "poids_total_echant_6"), ("poids_moyen_6", "prise_poids_total_6"), ("biomasse_7"),
                ],
            },
        ),
        
    )
            
    search_fields    = ('date',)

    


@admin.register(RationJournaliere)
class RationJournaliereAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    #list_fullwidth = True 
    warn_unsaved_form      = True 
    #list_display    = ['nom', 'aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5']
    list_display    = ['cycleProduction', 'infrastructure','quantite_ration_cycle1']
    #search_fields     = ('nom',)
    readonly_fields = ('quantite_ration_cycle1', 'quantite_ration_cycle2',
            'quantite_ration_cycle3', 'quantite_ration_cycle4', 
            'quantite_ration_cycle5', 'quantite_ration_cycle6'
                        # 'produit1', 'produit2', 'produit3', 'aliment1_cycle2', 
                        # 'aliment2_cycle2', 'aliment3_cycle2', 'aliment4_cycle2', 'aliment5_cycle2',
                        # 'produit1_cycle2', 'produit2_cycle2', 'produit3_cycle2'
                        )

    fieldsets = (

        (
            _("Infos Générales"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          ("cycleProduction", "infrastructure"),
                          
                          ("prixAliment1", "prixAliment2", ),
                          ("prixAliment3", "prixAliment4"),
                          ("prixAliment5"),
                          
                          ("prixProduit1", "prixProduit2"),
                          ("prixProduit3"),
                      ],
                  },
        ),

        

        (   
             _("Cycle 1"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle1", "taux_ration_cycle1"),
                          ("is_aliment1_cycle1", "is_aliment2_cycle1", "is_aliment3_cycle1"),
                          ("is_aliment4_cycle1", "is_aliment5_cycle1"),
                          
                          ("is_produit1_cycle1", "is_produit2_cycle1", "is_produit3_cycle1"),
                      ],
                  },
        ),          

        (   
             _("Cycle 2"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle2", "taux_ration_cycle2"),
                          ("is_aliment1_cycle2", "is_aliment2_cycle2", "is_aliment3_cycle2"),
                          ("is_aliment4_cycle2", "is_aliment5_cycle2"),
                          
                          ("is_produit1_cycle2", "is_produit2_cycle2", "is_produit3_cycle2"),
                      ],
                  },
        ),

        (   
             _("Cycle 3"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle3", "taux_ration_cycle3"),
                          ("is_aliment1_cycle3", "is_aliment2_cycle3", "is_aliment3_cycle3"),
                          ("is_aliment4_cycle3", "is_aliment5_cycle3"),
                          
                          ("is_produit1_cycle3", "is_produit2_cycle3", "is_produit3_cycle3"),
                      ],
                  },    
        ),

        (
            _("Cycle 4"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle4", "taux_ration_cycle4"),
                          ("is_aliment1_cycle4", "is_aliment2_cycle4", "is_aliment3_cycle4"),
                          ("is_aliment4_cycle4", "is_aliment5_cycle4"),
                          
                          ("is_produit1_cycle4", "is_produit2_cycle4", "is_produit3_cycle4"),
                      ],
                  },
        ),

        (
            _("Cycle 5"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle5", "taux_ration_cycle5"),
                          ("is_aliment1_cycle5", "is_aliment2_cycle5", "is_aliment3_cycle5"),
                          ("is_aliment4_cycle5", "is_aliment5_cycle5"),
                          
                          ("is_produit1_cycle5", "is_produit2_cycle5", "is_produit3_cycle5"),
                      ],
                  },
        ),

        (
            _("Cycle 6"),
                  {
                      "classes": ["tab"],
                      "fields": [
                        ("quantite_ration_cycle6", "taux_ration_cycle6"),
                          ("is_aliment1_cycle6", "is_aliment2_cycle6", "is_aliment3_cycle6"),
                          ("is_aliment4_cycle6", "is_aliment5_cycle6"),
                          
                          ("is_produit1_cycle6", "is_produit2_cycle6", "is_produit3_cycle6"),
                      ],
                  },
        ),

        
    )



@admin.register(Alevin)
class AlevinAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    readonly_fields = ('biomasse_tilapia', 'biomasse_claria', 'biomasse_autres')
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

    
# class QuartierInline(TabularInline):
#     model = Quartier
#     extra = 1

# class VilleInline(TabularInline):
#     model = Ville
#     extra = 1
#     #inlines = [QuartierInline]

# class CommuneInline(TabularInline):
#     model = Commune
#     extra = 1
#     #inlines = [VilleInline]

# class CercleInline(TabularInline):
#     model = Cercle
#     extra = 1
#     #inlines = [CommuneInline]

# class RegionInline(TabularInline):
#     model = Region
#     extra = 1
#     #inlines = [CercleInline]

@admin.register(Pays)
class PaysAdmin(ModelAdmin):
    inlines = [RegionInline]

# @admin.register(Pays)
# class PaysAdmin(ModelAdmin, nested_admin.NestedModelAdmin):
#     inlines = [RegionInline]

@admin.register(Region)
class RegionAdmin(ModelAdmin):
    inlines = [CercleInline]

@admin.register(Cercle)
class CercleAdmin(ModelAdmin):
    inlines = [CommuneInline]

@admin.register(Commune)
class CommuneAdmin(ModelAdmin):
    inlines = [VilleInline]

@admin.register(Ville)
class VilleAdmin(ModelAdmin):
    inlines = [QuartierInline]

@admin.register(Quartier)
class QuartierAdmin(ModelAdmin):
    #list_display = ['nom', 'ville', 'ville__commune', 'ville__commune__cercle', 'ville__commune__cercle__region', ]
    search_fields = ('nom',)
    list_filter = ('ville', 'ville__commune', 'ville__commune__cercle', 'ville__commune__cercle__region', 'ville__commune__cercle__region__pays')
    #autocomplete_fields = ['ville', 'ville__commune', 'ville__commune__cercle', 'ville__commune__cercle__region', 'ville__commune__cercle__region__pays']
    
    list_display = [
        'nom',
        'ville',
        'get_commune',
        'get_cercle',
        'get_region',
        'get_pays',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'ville__commune__cercle__region__pays'
        )

    def get_commune(self, obj):
        return obj.ville.commune.nom if obj.ville and obj.ville.commune else None
    get_commune.short_description = "Commune"

    def get_cercle(self, obj):
        commune = obj.ville.commune if obj.ville else None
        return commune.cercle.nom if commune and commune.cercle else None
    get_cercle.short_description = "Cercle"

    def get_region(self, obj):
        cercle = obj.ville.commune.cercle if obj.ville and obj.ville.commune else None
        return cercle.region.nom if cercle and cercle.region else None
    get_region.short_description = "Région"

    def get_pays(self, obj):
        region = obj.ville.commune.cercle.region if obj.ville and obj.ville.commune and obj.ville.commune.cercle else None
        return region.pays.nom if region and region.pays else None
    get_pays.short_description = "Pays"


@admin.register(AgentEncadrement)
class AgentEncadrementAdminClass(ImportExportModelAdmin, ModelAdmin):
    list_display = ['nom', 'prenom', 'adresse']
    inlines = [PisciculteurInline]


# @admin.register(DirecteurRegionale)
# class DirecteurRegionaleAdminClass(ImportExportModelAdmin, ModelAdmin):
#     list_display = ['nom', 'prenom', 'telephone']
#     inlines = [RegionInline]

@admin.register(ChefSecteur)
class ChefSecteurAdminClass(ImportExportModelAdmin, ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone']
    inlines = [ChefSecteurCercleInline]


@admin.register(DirecteurRegionale)
class DirecteurRegionaleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone')
    inlines = [AffectationRegionInline]


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(CustomUserAdmin, ModelAdmin):
    pass


@admin.register(Controlleur)
class ControlleurAdmin(ControlleurAdminClass, ModelAdmin):
    pass

# @admin.register(CyclesRation)
# class CyclesRationAdmin(ModelAdmin):
#     pass

# @admin.register(Ration1)
# class Ration1Admin(ModelAdmin):
#     pass

# @admin.register(Ration2)
# class Ration2Admin(ModelAdmin):
#     pass

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
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _


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
    extra = 1 
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
    extra = 1
    tab = True
    #fieldsets = [('Info 1', {'fields': ['date',], 'classes':['collapse']}), ('Info 2', {'fields': ['nombreEchantillons', 'nombreTotalPoissonsEchantillonnes', 'poidsTotalEchantillons'], 'classes': ['collapse']}),]
    
    

class AlevinTabularInline(TabularInline):
    model = Alevin
    show_change_link = True
    #per_page = 1
    extra = 1
    #tab = True


class RecolteTabularInline(TabularInline):
    model = Recolte
    show_change_link = True
    extra = 1
    #tab = True

class InfrastructureTabularInline(TabularInline):
    model = Infrastructure
    show_change_link = True
    extra = 1
    #tab = True


class CycleProductionTabularInline(TabularInline):
    model = CycleProduction
    show_change_link = True
    extra = 1


@admin.register(Pisciculteur)
class PisciculteurAdminClass(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter_submit = True
    # Display changelist in fullwidth
    #list_fullwidth = False

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
    #inlines = [InfrastructureTabularInline, ]
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
                PecheControleTabularInline, RecolteTabularInline ]
    
    #list_fullwidth = True 
    warn_unsaved_form    = True 
    list_display   = ['date', 'nom', 'ferme']
    search_fields   = ('nom',)


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
    list_display    = ['nom', 'aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5']
    search_fields     = ('nom',)

    fieldsets = (

        (
             _("Répartion entre types aliments"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "aliment1", "aliment2", "aliment3", "aliment4", "aliment5"
                      ],
                  },
        ),

        (
             _("Traitements sanitaires"),
                  {
                      "classes": ["tab"],
                      "fields": [
                          "produit1", "produit2"
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




@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
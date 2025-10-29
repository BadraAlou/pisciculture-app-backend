from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Pisciculteur, Quartier, AgentEncadrement, Ferme
from .widgets import AgentEncadrementFullNameWidget, PisciculteurFullNameWidget

class PisciculteurResource(resources.ModelResource):
    quartier_nom = fields.Field(
        column_name='quartier',
        attribute='quartier',
        widget=ForeignKeyWidget(Quartier, 'nom')
    )

    agent_nom = fields.Field(
        column_name='agent_encadrement',
        attribute='agent_encadrement',
        widget=ForeignKeyWidget(AgentEncadrement, 'nom')
    )

    class Meta:
        model = Pisciculteur
        fields = ('matricule', 'nom', 'prenom', 'genre', 'quartier_nom', 'agent_nom')
        export_order = ('matricule', 'nom', 'prenom', 'genre', 'quartier_nom', 'agent_nom')








class PisciculteurRawResource(resources.ModelResource):
    class Meta:
        model = Pisciculteur


class PisciculteurReadableResource(resources.ModelResource):
    quartier = fields.Field(
        column_name='Quartier',
        attribute='quartier',
        widget=ForeignKeyWidget(Quartier, 'nom')
    )
    agent_encadrement = fields.Field(
        column_name='Agent d\'Encadrement',
        attribute='agent_encadrement',
        #widget=ForeignKeyWidget(AgentEncadrement, 'nom')
        widget=AgentEncadrementFullNameWidget(AgentEncadrement, 'id')
    )

    class Meta:
        model = Pisciculteur
        fields = ('matricule', 'nom', 'prenom', 'genre', 'quartier', 'agent_encadrement')
        export_order = fields



class FermeResource(resources.ModelResource):
    quartier = fields.Field(
        column_name='Quartier',
        attribute='quartier',
        widget=ForeignKeyWidget(Quartier, 'nom')
    )
    pisciculteur = fields.Field(
        column_name='Pisciculteur',
        attribute='pisciculteur',
        #widget=ForeignKeyWidget(AgentEncadrement, 'nom')
        widget=PisciculteurFullNameWidget(Pisciculteur, 'id')
    )

    class Meta:
        model = Pisciculteur
        fields = ('nom', 'quartier', 'pisciculteur', 'coordonnees')
        export_order = fields





# Avec les titre personnalisés
"""class PisciculteurReadableResource(resources.ModelResource):
    matricule = fields.Field(
        column_name='Matricule',
        attribute='matricule'
    )
    nom = fields.Field(
        column_name='Nom',
        attribute='nom'
    )
    prenom = fields.Field(
        column_name='Prénom',
        attribute='prenom'
    )
    genre = fields.Field(
        column_name='Genre',
        attribute='genre'
    )
    quartier = fields.Field(
        column_name='Quartier',
        attribute='quartier',
        widget=ForeignKeyWidget(Quartier, 'nom')
    )
    agent_encadrement = fields.Field(
        column_name="Agent d'encadrement",
        attribute='agent_encadrement',
        widget=AgentEncadrementFullNameWidget(AgentEncadrement, 'id')
    )

    class Meta:
        model = Pisciculteur
        fields = (
            'matricule',
            'nom',
            'prenom',
            'genre',
            'quartier',
            'agent_encadrement',
        )
        export_order = fields
        """
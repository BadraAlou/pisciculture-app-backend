from django.db import models
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum




# Create your models here.
class Pisciculteur(models.Model):
    GENRES = [
        ('H', 'HOMME'),
        ('F', 'FEMME'),
    ]
    matricule = models.CharField(unique=True, max_length=20, blank=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, unique=True, blank=True)
    adresse = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, unique=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRES, blank=True)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'{self.nom} {self.prenom}'
    

class Zone(models.Model):
    nom = models.CharField(max_length=50,blank=True, null=True)
    pays = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    cercle = models.CharField(max_length=50, blank=True)
    commune = models.CharField(max_length=50, blank=True)
    ville = models.CharField(max_length=50, blank=True)
    quartier = models.CharField(max_length=50, blank=True)

    # Cette fonction affiche le nom de la zone
    def __str__(self):
        return f'{self.nom}'


class Ferme(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    pisciculteur = models.ForeignKey(Pisciculteur, on_delete=models.CASCADE)
    coordonnees = models.CharField(max_length=100, blank=True)
    
    # Cette fonction affiche le nom de la ferme
    def __str__(self):
        return f'{self.nom}'


# On crée une classe pour les type d'infrastrucutre avec comme attributs : le nom
class TypeInfrastructure(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    # Cette fonction affiche le nom de l'infrastructure
    def __str__(self):
        return f'{self.nom}'
    

# class AlevinsCycle:
#     def __init__(self, tilapia_bassin_en_ciment=0, tilapia_etang_en_terre=0, tilapia_bac_hors_sol=0,
#                  tilapia_cage_rectangulaire=0, tilapia_cage_circulaire=0,

#                 claria_bassin_en_ciment=0, claria_etang_en_terre=0, claria_bac_hors_sol=0,
#                 claria_cage_rectangulaire=0, claria_cage_circulaire=0,

#                 autres_bassin_en_ciment=0, autres_etang_en_terre=0, autres_bac_hors_sol=0,
#                 autres_cage_rectangulaire=0, autres_cage_circulaire=0,

#                 cout_tilapia_bassin_en_ciment=0, cout_tilapia_etang_en_terre=0, cout_tilapia_bac_hors_sol=0,
#                  cout_tilapia_cage_rectangulaire=0, cout_tilapia_cage_circulaire=0,

#                 cout_claria_bassin_en_ciment=0, cout_claria_etang_en_terre=0, cout_claria_bac_hors_sol=0,
#                 cout_claria_cage_rectangulaire=0, cout_claria_cage_circulaire=0,

#                 cout_autres_bassin_en_ciment=0, cout_autres_etang_en_terre=0, cout_autres_bac_hors_sol=0,
#                 cout_autres_cage_rectangulaire=0, cout_autres_cage_circulaire=0,
#             ) :
        
#         self.tilapia_bassin_en_ciment = tilapia_bassin_en_ciment
#         self.tilapia_etang_en_terre = tilapia_etang_en_terre
#         self.tilapia_bac_hors_sol = tilapia_bac_hors_sol
#         self.tilapia_cage_rectangulaire = tilapia_cage_rectangulaire
#         self.tilapia_cage_circulaire = tilapia_cage_circulaire

#         self.claria_bassin_en_ciment = claria_bassin_en_ciment
#         self.claria_etang_en_terre = claria_etang_en_terre
#         self.claria_bac_hors_sol = claria_bac_hors_sol
#         self.claria_cage_rectangulaire = claria_cage_rectangulaire
#         self.claria_cage_circulaire = claria_cage_circulaire

#         self.autres_bassin_en_ciment = autres_bassin_en_ciment
#         self.autres_etang_en_terre = autres_etang_en_terre
#         self.autres_bac_hors_sol = autres_bac_hors_sol
#         self.autres_cage_rectangulaire = autres_cage_rectangulaire
#         self.autres_cage_circulaire = autres_cage_circulaire

#         self.cout_tilapia_bassin_en_ciment = cout_tilapia_bassin_en_ciment
#         self.cout_tilapia_etang_en_terre = cout_tilapia_etang_en_terre
#         self.cout_tilapia_bac_hors_sol = cout_tilapia_bac_hors_sol
#         self.cout_tilapia_cage_rectangulaire = cout_tilapia_cage_rectangulaire
#         self.cout_tilapia_cage_circulaire = cout_tilapia_cage_circulaire

#         self.cout_claria_bassin_en_ciment = cout_claria_bassin_en_ciment
#         self.cout_claria_etang_en_terre = cout_claria_etang_en_terre
#         self.cout_claria_bac_hors_sol = cout_claria_bac_hors_sol
#         self.cout_claria_cage_rectangulaire = cout_claria_cage_rectangulaire
#         self.cout_claria_cage_circulaire = cout_claria_cage_circulaire

#         self.cout_autres_bassin_en_ciment = cout_autres_bassin_en_ciment
#         self.cout_autres_etang_en_terre = cout_autres_etang_en_terre
#         self.cout_autres_bac_hors_sol = cout_autres_bac_hors_sol
#         self.cout_autres_cage_rectangulaire = cout_autres_cage_rectangulaire
#         self.cout_autres_cage_circulaire = cout_autres_cage_circulaire

#     def __str__(self):
#         return (f"Tilapia (Bassin): {self.tilapia_bassin}, Claria (Bassin): {self.claria_bassin}, "
#                 f"Tilapia (Cage): {self.tilapia_cage}, Claria (Cage): {self.claria_cage}")
    
#     def totalBassinCiment(self):
#         return intcomma(self.tilapia_bassin_en_ciment + self.claria_bassin_en_ciment + self.autres_bassin_en_ciment)
#     def totalEtangTerre(self):
#         return intcomma(self.tilapia_etang_en_terre + self.claria_etang_en_terre + self.autres_etang_en_terre)
#     def totalBacHorsSol(self):
#         return intcomma(self.tilapia_bac_hors_sol + self.claria_bac_hors_sol + self.autres_bac_hors_sol)
#     def totalCageRectangulaire(self):
#         return intcomma(self.tilapia_cage_rectangulaire + self.claria_cage_rectangulaire + self.autres_cage_rectangulaire)
#     def totalCageCirculaire(self):
#         return intcomma(self.tilapia_cage_circulaire + self.claria_cage_circulaire + self.autres_cage_circulaire)
    
#     def coutTotalBassinCiment(self):
#         return intcomma(self.cout_tilapia_bassin_en_ciment + self.cout_claria_bassin_en_ciment + self.cout_autres_bassin_en_ciment)
#     def coutTotalEtangTerre(self):
#         return intcomma(self.cout_tilapia_etang_en_terre + self.cout_claria_etang_en_terre + self.cout_autres_etang_en_terre)
#     def coutTotalBacHorsSol(self):
#         return intcomma(self.cout_tilapia_bac_hors_sol + self.cout_claria_bac_hors_sol + self.cout_autres_bac_hors_sol)
#     def coutTotalCageRectangulaire(self):
#         return intcomma(self.cout_tilapia_cage_rectangulaire + self.cout_claria_cage_rectangulaire + self.cout_autres_cage_rectangulaire)
#     def coutTotalCageCirculaire(self):
#         return intcomma(self.cout_tilapia_cage_circulaire + self.cout_claria_cage_circulaire + self.cout_autres_cage_circulaire)
    
#     def totalNombreAlevins(self):
#         print(f'*** Yo total nombres : {self.totalBassinCiment()  + self.totalBacHorsSol() + self.totalCageRectangulaire() + self.totalCageCirculaire()}')
#         return intcomma(
#             self.tilapia_bassin_en_ciment + self.claria_bassin_en_ciment + self.autres_bassin_en_ciment +
#             self.tilapia_etang_en_terre + self.claria_etang_en_terre + self.autres_etang_en_terre +
#             self.tilapia_bac_hors_sol + self.claria_bac_hors_sol + self.autres_bac_hors_sol +
#             self.tilapia_cage_rectangulaire + self.claria_cage_rectangulaire + self.autres_cage_rectangulaire +
#             self.tilapia_cage_circulaire + self.claria_cage_circulaire + self.autres_cage_circulaire

#         )
#     def totalCoutAlevins(self):
        #return intcomma(self.coutTotalBassinCiment() + self.coutTotalEtangTerre() + self.coutTotalBacHorsSol() + self.coutTotalCageRectangulaire() + self.coutTotalCageCirculaire())
        return intcomma(
            self.cout_tilapia_bassin_en_ciment + self.cout_claria_bassin_en_ciment + self.cout_autres_bassin_en_ciment +
            self.cout_tilapia_etang_en_terre + self.cout_claria_etang_en_terre + self.cout_autres_etang_en_terre +
            self.cout_tilapia_bac_hors_sol + self.cout_claria_bac_hors_sol + self.cout_autres_bac_hors_sol +
            self.cout_tilapia_cage_rectangulaire + self.cout_claria_cage_rectangulaire + self.cout_autres_cage_rectangulaire +
            self.cout_tilapia_cage_circulaire + self.cout_claria_cage_circulaire + self.cout_autres_cage_circulaire

        )


class AlevinsCycle:
    def __init__(self, data=None):
        # Structure des données : { 'poisson': { 'structure': valeur } }
        poissons = ['tilapia', 'claria', 'autres']
        structures = ['bassin_en_ciment', 'etang_en_terre', 'bac_hors_sol', 'cage_rectangulaire', 'cage_circulaire']

        # Initialisation des données
        self.alevins = {poisson: {structure: 0 for structure in structures} for poisson in poissons}
        self.couts = {poisson: {structure: 0 for structure in structures} for poisson in poissons}

        if data:
            for poisson, structures_data in data.get('alevins', {}).items():
                if poisson in self.alevins:
                    self.alevins[poisson].update(structures_data)

            for poisson, structures_data in data.get('couts', {}).items():
                if poisson in self.couts:
                    self.couts[poisson].update(structures_data)

    def total_par_structure(self, poisson_type, structure_type):
        return self.alevins[poisson_type][structure_type]

    def total_cout_par_structure(self, poisson_type, structure_type):
        return self.couts[poisson_type][structure_type]

    def total_general_alevins(self):
        return sum(
            sum(structures.values()) for structures in self.alevins.values()
        )

    def total_general_cout(self):
        return sum(
            sum(structures.values()) for structures in self.couts.values()
        )

    def total_par_structure_generale(self, structure_type):
        return sum(self.alevins[poisson][structure_type] for poisson in self.alevins)

    def total_cout_par_structure_generale(self, structure_type):
        return sum(self.couts[poisson][structure_type] for poisson in self.couts)

    def get_summary(self):
        return {
            "total_alevins": self.total_general_alevins(),
            "total_couts": self.total_general_cout(),
            "par_structure": {
                structure: {
                    "total_alevins": self.total_par_structure_generale(structure),
                    "total_cout": self.total_cout_par_structure_generale(structure)
                } for structure in self.alevins['tilapia']
            }
        }

    def __str__(self):
        summary = self.get_summary()
        return f"Total alevins: {summary['total_alevins']}, Total couts: {summary['total_couts']}"

    def get_production_summary_optimized(self, cycle):
        from django.db.models import Sum
        #from myapp.models import Alevin  # Remplacez par le bon chemin de votre modèle

        aggregations = Alevin.objects.filter(cycleProduction=cycle).values(
            'infrastructure__typeInfrastructure__nom'
        ).annotate(
            total_tilapia=Sum('nombreTilapia'),
            total_claria=Sum('nombreClaria'),
            total_autres=Sum('nombreAutres'),
            cout_tilapia=Sum('coutAchatTilapia'),
            cout_claria=Sum('coutAchatClaria'),
            cout_autres=Sum('coutAchatAutres')
        )

        for entry in aggregations:
            type_infra = entry['infrastructure__typeInfrastructure__nom'].lower().replace(' ', '_')
            self.alevins['tilapia'][type_infra] = entry.get('total_tilapia', 0)
            self.alevins['claria'][type_infra] = entry.get('total_claria', 0)
            self.alevins['autres'][type_infra] = entry.get('total_autres', 0)
            self.couts['tilapia'][type_infra] = entry.get('cout_tilapia', 0)
            self.couts['claria'][type_infra] = entry.get('cout_claria', 0)
            self.couts['autres'][type_infra] = entry.get('cout_autres', 0)

        return self


 # On crée une classe pour les cycle de Production avec comme attributs : la date et le nom
class CycleProduction(models.Model):
    CYCLES = [
        ('ENCOURS', 'ENCOURS'),
        ('TERMINE', 'TERMINE'),
    ]
    date = models.DateField(default=datetime.today, verbose_name="Date de mise en charge")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin de cycle")
    nom = models.CharField(max_length=50, blank=True)
    #infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)
    #cycle = models.BooleanField(default=False, verbose_name="Valider la fin de cycle")
    cycle = models.CharField(max_length=20, choices=CYCLES, default='ENCOURS')

    # Cette fonction affiche le nom du cycle de production
    def __str__(self):
        return f'{self.nom}'
    
    def get_nombre_tilapia_par_type_infrastructure(self, type_infrastructure_nom):
        
        return Alevin.objects.filter(
            cycleProduction=self,
            infrastructure__typeInfrastructure__nom=type_infrastructure_nom
        ).aggregate(total_tilapia=Sum('nombreTilapia'))['total_tilapia'] or 0
    
    # def get_total_alevin_by_infrastructure(self, field_name, type_infrastructure_nom):
    #     """
    #     Récupère la somme d'un champ donné pour une infrastructure spécifique.
        
    #     :param field_name: Nom du champ à agréger (ex : 'nombreTilapia', 'nombreClaria')
    #     :param type_infrastructure_nom: Nom du type d'infrastructure (ex : 'Bassin en ciment')
    #     :return: Somme des valeurs du champ ou 0 si aucune donnée trouvée
    #     """
    #     if not hasattr(Alevin, field_name):
    #         raise ValueError(f"Le champ '{field_name}' n'existe pas dans le modèle Alevin.")
        
    #     return Alevin.objects.filter(
    #         cycleProduction=self,
    #         infrastructure__typeInfrastructure__nom=type_infrastructure_nom
    #     ).aggregate(total=Sum(field_name))['total'] or 0

    def get_total_alevin_by_infrastructure(self, field_name, type_infrastructure_nom):
        """
        Récupère la somme d'un champ donné pour une infrastructure spécifique, insensible à la casse et aux espaces.
        
        :param field_name: Nom du champ à agréger (ex : 'nombreTilapia', 'nombreClaria')
        :param type_infrastructure_nom: Nom du type d'infrastructure (ex : 'Bassin en ciment')
        :return: Somme des valeurs du champ ou 0 si aucune donnée trouvée
        """
        if not hasattr(Alevin, field_name):
            raise ValueError(f"Le champ '{field_name}' n'existe pas dans le modèle Alevin.")
        
        # Normalisation du type d'infrastructure
        type_infrastructure_nom = type_infrastructure_nom.strip().lower()

        return Alevin.objects.filter(
            cycleProduction=self,
            infrastructure__typeInfrastructure__nom__iexact=type_infrastructure_nom
        ).aggregate(total=Sum(field_name))['total'] or 0
    

    # def get_production_summary(self):
    #     """
    #     Crée un résumé de la production pour Tilapia et Claria par type d'infrastructure.
    #     """
    #     summary = AlevinsCycle()

    #     # Récupération des valeurs pour chaque combinaison
    #     summary.tilapia_bassin_en_ciment = self.get_total_alevin_by_infrastructure('nombreTilapia', 'Bassin en ciment')
    #     summary.claria_bassin_en_ciment = self.get_total_alevin_by_infrastructure('nombreClaria', 'Bassin en ciment')
    #     summary.autres_bassin_en_ciment = self.get_total_alevin_by_infrastructure('nombreAutres', 'Bassin en ciment')
    #     summary.cout_tilapia_bassin_en_ciment = self.get_total_alevin_by_infrastructure('coutAchatTilapia', 'Bassin en ciment')
    #     summary.cout_claria_bassin_en_ciment = self.get_total_alevin_by_infrastructure('coutAchatClaria', 'Bassin en ciment')
    #     summary.cout_autres_bassin_en_ciment = self.get_total_alevin_by_infrastructure('coutAchatAutres', 'Bassin en ciment')

    #     summary.tilapia_etang_en_terre = self.get_total_alevin_by_infrastructure('nombreTilapia', 'Etang en Terre')
    #     summary.claria_etang_en_terre = self.get_total_alevin_by_infrastructure('nombreClaria', 'Etang en Terre')
    #     summary.autres_etang_en_terre = self.get_total_alevin_by_infrastructure('nombreAutres', 'Etang en Terre')
    #     summary.cout_tilapia_etang_en_terre = self.get_total_alevin_by_infrastructure('coutAchatTilapia', 'Etang en Terre')
    #     summary.cout_claria_etang_en_terre = self.get_total_alevin_by_infrastructure('coutAchatClaria', 'Etang en Terre')
    #     summary.cout_autres_etang_en_terre = self.get_total_alevin_by_infrastructure('coutAchatAutres', 'Etang en Terre')

    #     summary.tilapia_bac_hors_sol = self.get_total_alevin_by_infrastructure('nombreTilapia', 'Bac hors sol')
    #     summary.claria_bac_hors_sol = self.get_total_alevin_by_infrastructure('nombreClaria', 'Bac hors sol')
    #     summary.autres_bac_hors_sol = self.get_total_alevin_by_infrastructure('nombreAutres', 'Bac hors sol')
    #     summary.cout_tilapia_bac_hors_sol = self.get_total_alevin_by_infrastructure('coutAchatTilapia', 'Bac hors sol')
    #     summary.cout_claria_bac_hors_sol = self.get_total_alevin_by_infrastructure('coutAchatClaria', 'Bac hors sol')
    #     summary.cout_autres_bac_hors_sol = self.get_total_alevin_by_infrastructure('coutAchatAutres', 'Bac hors sol')

    #     summary.tilapia_cage_rectangulaire = self.get_total_alevin_by_infrastructure('nombreTilapia', 'Cage Rectangulaire')
    #     summary.claria_cage_rectangulaire = self.get_total_alevin_by_infrastructure('nombreClaria', 'Cage Rectangulaire')
    #     summary.autres_cage_rectangulaire = self.get_total_alevin_by_infrastructure('nombreAutres', 'Cage Rectangulaire')
    #     summary.cout_tilapia_cage_rectangulaire = self.get_total_alevin_by_infrastructure('coutAchatTilapia', 'Cage Rectangulaire')
    #     summary.cout_claria_cage_rectangulaire = self.get_total_alevin_by_infrastructure('coutAchatClaria', 'Cage Rectangulaire')
    #     summary.cout_autres_cage_rectangulaire = self.get_total_alevin_by_infrastructure('coutAchatAutres', 'Cage Rectangulaire')

    #     summary.tilapia_cage_circulaire = self.get_total_alevin_by_infrastructure('nombreTilapia', 'Cage Circulaire')
    #     summary.claria_cage_circulaire = self.get_total_alevin_by_infrastructure('nombreClaria', 'Cage Circulaire')
    #     summary.autres_cage_circulaire = self.get_total_alevin_by_infrastructure('nombreAutres', 'Cage Circulaire')
    #     summary.cout_tilapia_cage_circulaire = self.get_total_alevin_by_infrastructure('coutAchatTilapia', 'Cage Circulaire')
    #     summary.cout_claria_cage_circulaire = self.get_total_alevin_by_infrastructure('coutAchatClaria', 'Cage Circulaire')
    #     summary.cout_autres_cage_circulaire = self.get_total_alevin_by_infrastructure('coutAchatAutres', 'Cage Circulaire')

    #     return summary

    def get_production_summary(self):
        INFRASTRUCTURE_TYPES = [
            'Bassin en ciment',
            'Etang en Terre',
            'Bac hors sol',
            'Cage Rectangulaire',
            'Cage Circulaire',
        ]
        summary = AlevinsCycle()
        champs = ['nombreTilapia', 'nombreClaria', 'nombreAutres', 
                'coutAchatTilapia', 'coutAchatClaria', 'coutAchatAutres']

        for infrastructure_type in INFRASTRUCTURE_TYPES:
            print(print(f'*** yo infras type : {infrastructure_type}'))
            infrastructure_key = infrastructure_type.lower().replace(' ', '_')
            #infrastructure_key = infrastructure_type.lower()
            for champ in champs:
                #print(f'*** yo champ : {champ}')
                valeur = self.get_total_alevin_by_infrastructure(champ, infrastructure_type)
                
                setattr(summary, f'{champ}_{infrastructure_key}', valeur)

        print(print(f'*** *** yo valeur  : {summary.nombreTilapia_bassin_en_ciment}'))
        return summary


    def get_production_summary_optimized(self):
        summary = AlevinsCycle()
        aggregations = Alevin.objects.filter(cycleProduction=self).values(
            'infrastructure__typeInfrastructure__nom'
        ).annotate(
            total_tilapia=Sum('nombreTilapia'),
            total_claria=Sum('nombreClaria'),
            total_autres=Sum('nombreAutres'),
            cout_tilapia=Sum('coutAchatTilapia'),
            cout_claria=Sum('coutAchatClaria'),
            cout_autres=Sum('coutAchatAutres')
        )

        for entry in aggregations:
            type_infra = entry['infrastructure__typeInfrastructure__nom'].lower().replace(' ', '_')
            setattr(summary, f'tilapia_{type_infra}', entry.get('total_tilapia', 0))
            setattr(summary, f'claria_{type_infra}', entry.get('total_claria', 0))
            setattr(summary, f'autres_{type_infra}', entry.get('total_autres', 0))
            setattr(summary, f'cout_tilapia_{type_infra}', entry.get('cout_tilapia', 0))
            setattr(summary, f'cout_claria_{type_infra}', entry.get('cout_claria', 0))
            setattr(summary, f'cout_autres_{type_infra}', entry.get('cout_autres', 0))

        print(dfg)
        
        return summary
    

    
    
# On crée une classe pour les infrastructures avec comme attributs : type, superficie, volume, numero, dateConstruction, dateReabilitation et natureReabilitation
class Infrastructure(models.Model):
    #ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    typeInfrastructure = models.ForeignKey(TypeInfrastructure, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    superficie = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    dateConstruction = models.DateField(blank=True, null=True)
    dateReabilitation = models.DateField(blank=True, null=True)
    natureReabilitation = models.CharField(max_length=50, blank=True)
    
    # Cette fonction affiche le nom de l'infrastructure
    def __str__(self):
        return f'{self.numero}'
    

# On crée une classe pour les types d'Alevin avec comme attributs : le nom
class TypeAlevin(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    # Cette fonction affiche le nom de l'alévin
    def __str__(self):
        return f'{self.nom}'
    


# On crée une classe pour les Infos d'Alevin avec comme attributs : nombre, cout d'achat, biomasse
class Alevin(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)
    # nombre
    nombreTilapia = models.PositiveIntegerField(verbose_name="Nombre Tilapia", default=0)
    nombreClaria = models.PositiveIntegerField(verbose_name="Nombre Claria", default=0)
    nombreAutres = models.PositiveIntegerField(verbose_name="Nombre Autres", default=0)
    # cout d'achat
    coutAchatTilapia = models.PositiveIntegerField(verbose_name="Coût Achat Tilapia", default=0)
    coutAchatClaria = models.PositiveIntegerField(verbose_name="Coût Achat Claria", default=0)
    coutAchatAutres = models.PositiveIntegerField(verbose_name="Coût Achat Autres", default=0)
    # mortalité
    mortaliteTilapia = models.PositiveIntegerField(verbose_name="Mortalité Tilapia", default=0)
    mortaliteClaria = models.PositiveIntegerField(verbose_name="Mortalité Claria", default=0)
    mortaliteAutres = models.PositiveIntegerField(verbose_name="Mortalité Autres", default=0)

    # remplace mortalité
    remplaceMortaliteTilapia = models.PositiveIntegerField(verbose_name="Remplace Mortalité Tilapia", default=0)
    remplaceMortaliteClaria = models.PositiveIntegerField(verbose_name="Remplace Mortalité Claria", default=0)
    remplaceMortaliteAutres = models.PositiveIntegerField(verbose_name="Remplace Mortalité Autres", default=0)

    # biomasse
    biomasseTilapia = models.PositiveIntegerField(verbose_name="Biomasse Tilapia", default=0)
    biomasseClaria = models.PositiveIntegerField(verbose_name="Biomasse Claria", default=0)
    biomasseAutres = models.PositiveIntegerField(verbose_name="Biomasse Autres", default=0)

    # poids moyen
    poidsMoyenTilapia = models.PositiveIntegerField(verbose_name="Poids Moyen Tilapia", default=0)
    poidsMoyenClaria = models.PositiveIntegerField(verbose_name="Poids Moyen Claria", default=0)
    poidsMoyenAutres = models.PositiveIntegerField(verbose_name="Poids Moyen Autres", default=0)

    def __str__(self):
        return super().__str__()
    
    def coutTotalTilapia(self):
        return intcomma(self.nombreTilapia * self.coutAchatTilapia)
    
    def coutTotalClaria(self):
        return intcomma(self.nombreClaria * self.coutAchatClaria)
    
    def coutTotalAutres(self):
        return intcomma(self.nombreAutres * self.coutAchatAutres)
    
    def coutTotalAlevins(self):
        return intcomma(self.coutTotalTilapia() + self.coutTotalClaria() + self.coutTotalAutres())


# On crée une classe pour les ration journalieres avec comme attributs: 
class PecheControle(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)

    date = models.DateField(default=datetime.today)
    nombreEchantillons = models.PositiveIntegerField(verbose_name="Nombre d'échantillons", default=0)
    nombreTotalPoissonsEchantillonnes = models.PositiveIntegerField(verbose_name="Nombre total poissons échantillonnés", default=0)
    poidsTotalEchantillons = models.FloatField(verbose_name="Poids moyen", default=0)
    poidsMoyen = models.FloatField(verbose_name="Poids Total des echantillons", default=0)
    prisePoidsTotal = models.FloatField(verbose_name="Prise poids total", default=0)
    biomasse = models.PositiveIntegerField(verbose_name="Biomasse",default=0)

    # Cette fonction affiche le nom du cycle de production
    # def __str__(self):
    #     return f'{self.nom}'

class Aliment(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Aliment")
    quantite = models.FloatField(default=0)
    prix = models.PositiveIntegerField(verbose_name="Prix Aliment", default=0)

    def __str__(self):
        return f'{self.nom}'


class Produit(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Produit")
    quantite = models.FloatField(default=0)
    prix = models.PositiveIntegerField(verbose_name="Prix Produit", default=0)

    def __str__(self):
        return f'{self.nom}'
    

class Charges(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    eau = models.PositiveIntegerField(verbose_name="Total Eau", default=0)
    main_oeuvre = models.PositiveIntegerField(verbose_name="Total Main d'oeuvre", default=0)
    amortissements = models.PositiveIntegerField(verbose_name="Total Amortissement", default=0)

    # def __str__(self):
    #     return f'{self.nom}'
    def coutTotalCharges(self):
        return intcomma(self.eau + self.main_oeuvre + self.amortissements)



# On crée une classe pour les ration journalieres avec comme attributs: date, aliment1, aliment2, aliment3, aliment4 (aliment = float)
class RationJournaliere(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)
    nom = models.CharField(max_length=50, verbose_name="Nom Ration Journalière", blank=True)
    aliment1 = models.FloatField(verbose_name="Aliment 1", default=0)
    prixAliment1 = models.PositiveIntegerField(verbose_name="Prix Aliment 1", default=0)
    aliment2 = models.FloatField(verbose_name="Aliment 2", default=0)
    prixAliment2 = models.PositiveIntegerField(verbose_name="Prix Aliment 2", default=0)
    aliment3 = models.FloatField(verbose_name="Aliment 3", default=0)
    prixAliment3 = models.PositiveIntegerField(verbose_name="Prix Aliment 3", default=0)
    aliment4 = models.FloatField(verbose_name="Aliment 4", default=0)
    prixAliment4 = models.PositiveIntegerField(verbose_name="Prix Aliment 4", default=0)
    aliment5 = models.FloatField(verbose_name="Aliment 5", default=0)
    prixAliment5 = models.PositiveIntegerField(verbose_name="Prix Aliment 5", default=0)
    produit1 = models.FloatField(verbose_name="Produit 1", default=0, blank=True)
    prixProduit1 = models.PositiveIntegerField(verbose_name="Prix Produit 1", default=0)
    produit2 = models.FloatField(verbose_name="Produit 2", default=0, blank=True)
    prixProduit2 = models.PositiveIntegerField(verbose_name="Prix Produit 2", default=0)
    produit3 = models.FloatField(verbose_name="Produit 3", default=0, blank=True)
    prixProduit3 = models.PositiveIntegerField(verbose_name="Prix Produit 3", default=0)

    #Cette fonction affiche le nom du cycle de production
    def __str__(self):
        return f'{self.nom}'
    
    def coutTotalAliment(self):
        return intcomma(self.prixAliment1 + self.prixAliment2 + self.prixAliment3 + self.prixAliment4 + self.prixAliment5)
    
    def coutTotalProduit(self):
        return intcomma(self.prixProduit1 + self.prixProduit2 + self.prixProduit3)

    

# On crée une classe recolte avec les attributs: dateVente, poidsTotalVente, recette, dateDon, poidsTotalDon, dateAutoConsommation, poidsTotalAutoConsommation
class Recolte(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)
    # Tilapia
    dateVenteTilapia = models.DateField(verbose_name="Tilapia - Date vente", default=datetime.today)
    poidsTotalVenteTilapia  = models.FloatField(verbose_name="Poids total vendu",default=0, blank=True)
    recetteTilapia = models.FloatField(verbose_name="Recette",default=0, blank=True)
    dateDonTilapia = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonTilapia  = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationTilapia = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationTilapia  = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True)

    # Clarias
    dateVenteClarias = models.DateField(verbose_name="Clarias - Date de vente", default=datetime.today)
    poidsTotalVenteClarias   = models.FloatField(verbose_name="Poids total vendu",default=0, blank=True)
    recetteClarias  = models.FloatField(verbose_name="Recette",default=0, blank=True)
    dateDonClarias  = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonClarias   = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationClarias  = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationClarias   = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True)

    # Autres
    dateVenteAutres  = models.DateField(verbose_name="Autres - Date de vente", default=datetime.today)
    poidsTotalVenteAutres    = models.FloatField(verbose_name="Poids total vendu",default=0, blank=True)
    recetteAutres    = models.FloatField(verbose_name="Recette",default=0, blank=True)
    dateDonAutres    = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonAutres      = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationAutres    = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationAutres       = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True)

    def quantiteTotalVente(self):
        return intcomma(self.poidsTotalVenteTilapia + self.poidsTotalVenteClarias + self.poidsTotalVenteAutres)

    def recetteTotalVente(self):
        return intcomma(self.recetteTilapia + self.recetteClarias + self.recetteAutres)

    def quantiteTotalDon(self):
        return intcomma(self.poidsTotalDonTilapia + self.poidsTotalDonClarias + self.poidsTotalDonAutres)
    
    def quantiteTotalAutoConsommation(self):
        return intcomma(self.poidsTotalAutoConsommationTilapia + self.poidsTotalAutoConsommationClarias + self.poidsTotalAutoConsommationAutres)

    def recetteTotal(self):
        return self.recetteTotalVente()

class Dashboard(models.Model):
    nom = models.CharField(max_length=50)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'{self.nom}'



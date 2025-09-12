from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime, timedelta
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum
import uuid
#from smart_selects.db_fields import ChainedForeignKey
# Create your models here.


class Pays(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Region(models.Model):
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='regions')
    nom = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.nom} ({self.pays.nom})"


class Cercle(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cercles')
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

# class Cercle(models.Model):
#     pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
#     region = ChainedForeignKey(
#         Region,
#         chained_field="pays",
#         chained_model_field="pays",
#         show_all=False,
#         auto_choose=True,
#         sort=True,
#         on_delete=models.CASCADE
#     )
#     nom = models.CharField(max_length=100)


class Commune(models.Model):
    cercle = models.ForeignKey(Cercle, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.cercle.nom})"


class Ville(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"


class Quartier(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.ville.nom})"


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, telephone=None, password=None, **extra_fields):
        if not email and not telephone:
            raise ValueError('Un email ou un téléphone est requis')
        email = self.normalize_email(email)
        user = self.model(email=email, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, telephone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, telephone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # ou 'telephone', selon ton choix
    REQUIRED_FIELDS = ['telephone']  # ou []

    def __str__(self):
        return self.email or self.telephone


class ChefSecteurCercle(models.Model):
    chef_secteur = models.ForeignKey('ChefSecteur', on_delete=models.CASCADE)
    cercle = models.ForeignKey('Cercle', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('chef_secteur', 'cercle')

    def __str__(self):
        return f"{self.chef_secteur.nom} - {self.cercle.nom}"


class ChefSecteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='chef_secteur_profile')
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, blank=True, null=True, unique=True)
    #cercle = models.ManyToManyField(Cercle, blank=True)
    cercles = models.ManyToManyField('Cercle', through='ChefSecteurCercle', blank=True)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        #return f'Agent Encadrement : {self.nom} {self.prenom}'
        return self.nom




# class DirecteurRegionale(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='directeur_regionnale_profile')
#     nom = models.CharField(max_length=50)
#     prenom = models.CharField(max_length=50)
#     telephone = models.CharField(max_length=50, blank=True, null=True, unique=True)
#     region = models.ManyToManyField(Region, blank=True)

#     # Cette fonction affiche le nom et le prenom du pisciculteur
#     def __str__(self):
#         #return f'Agent Encadrement : {self.nom} {self.prenom}'
#         return self.nom


class AffectationRegionDirecteur(models.Model):
    directeur = models.ForeignKey("DirecteurRegionale", on_delete=models.CASCADE)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    date_affectation = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('directeur', 'region')

    def __str__(self):
        return f"{self.directeur.nom} → {self.region.nom}"


class DirecteurRegionale(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='directeur_regionnale_profile')
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, blank=True, null=True, unique=True)

    # Table intermédiaire personnalisée ici
    region = models.ManyToManyField(Region, through='AffectationRegionDirecteur', blank=True)
    #region = models.ManyToManyField(Region, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"



class AgentEncadrement(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_encadrement_profile')
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50, blank=True)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'Agent Encadrement : {self.nom} {self.prenom}'



class Pisciculteur(models.Model):
    GENRES = [
        ('H', 'HOMME'),
        ('F', 'FEMME'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pisciculteur_profile')

    matricule = models.CharField(unique=True, max_length=20, blank=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    #telephone = models.CharField(max_length=50, unique=True, blank=True)
    adresse = models.CharField(max_length=50, blank=True)
    #email = models.EmailField(max_length=50, unique=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRES, blank=True)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, blank=True, null=True)
    agent_encadrement = models.ForeignKey(AgentEncadrement, on_delete=models.CASCADE, blank=True, null=True)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'{self.nom} {self.prenom}'

    def save(self, *args, **kwargs):
        # Géneration automatique du matricule
        if not self.matricule:
            self.matricule = f"PC-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class Controlleur(models.Model):
    CATEGORIES = [
        #('AE', 'AGENT ENCADREMENT'),
        ('CS', 'CHEF SECTEUR'),
        ('DR', 'DIRECTEUR REGIONALE'),
        ('S', 'SUPERVISEUR'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='controlleur_profile')
    categorie = models.CharField(max_length=2, choices=CATEGORIES)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50, blank=True)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'{self.nom} {self.prenom}'









# class Zone(models.Model):
#     nom = models.CharField(max_length=50,blank=True, null=True)
#     pays = models.CharField(max_length=50, blank=True)
#     region = models.CharField(max_length=50, blank=True)
#     cercle = models.CharField(max_length=50, blank=True)
#     commune = models.CharField(max_length=50, blank=True)
#     ville = models.CharField(max_length=50, blank=True)
#     quartier = models.CharField(max_length=50, blank=True)

#     # Cette fonction affiche le nom de la zone
#     def __str__(self):
#         return f'{self.nom}'


class Ferme(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    #zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, blank=True, null=True)
    pisciculteur = models.ForeignKey(Pisciculteur, on_delete=models.CASCADE)
    coordonnees = models.CharField(max_length=100, blank=True)
    
    # Cette fonction affiche le nom de la ferme
    def __str__(self):
        return f'{self.nom}'


# On crée une classe pour les type d'infrastrucutre avec comme attributs : le nom
class TypeInfrastructure(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)  # ex: "CR", "BT", etc.

    # Cette fonction affiche le nom de l'infrastructure
    def __str__(self):
        return f'{self.nom}'
    

# class RationJournaliereCycle:
#     def __init__(self, data=None):
#         # Initialisation dynamique via un dictionnaire
#         self.data = data or {
#             'tilapia': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                         'cage_rectangulaire': 0, 'cage_circulaire': 0},
#             'claria': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                        'cage_rectangulaire': 0, 'cage_circulaire': 0},
#             'autres': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                        'cage_rectangulaire': 0, 'cage_circulaire': 0},
#             'couts': {
#                 'tilapia': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                             'cage_rectangulaire': 0, 'cage_circulaire': 0},
#                 'claria': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
#                 'autres': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0,
#                            'cage_rectangulaire': 0, 'cage_circulaire': 0}
#             },
#         }

#         # Initialisation des variables
#         self.nb_total_ration = 0
#         self.cout_total_ration = 0

#     def calculer_totaux(self):
#         """Calcule les totaux des rations et coûts."""
#         self.nb_total_ration = self.total_general()
#         self.cout_total_ration = self.total_general_cout()

#     def nombre_total_ration(self, infrastructure_type):
#         """Calcule le total des rations pour un type d'infrastructure."""
#         return sum(self.data.get(fish_type, {}).get(infrastructure_type, 0)
#                    for fish_type in ['tilapia', 'claria', 'autres'])

#     def cout_total_ration_infrastructure(self, infrastructure_type):
#         """Calcule le coût total des rations pour une infrastructure donnée."""
#         return sum(self.data['couts'].get(fish_type, {}).get(infrastructure_type, 0)
#                    for fish_type in ['tilapia', 'claria', 'autres'])

#     def total_type(self, fish_type):
#         """Calcule le total des rations pour un type donné (tilapia, claria, autres)."""
#         return sum(self.data[fish_type].values())

#     def total_cout_type(self, fish_type):
#         """Calcule le total des coûts pour un type donné."""
#         return sum(self.data['couts'][fish_type].values())

#     def total_general(self):
#         """Calcule le total général des rations."""
#         return sum(self.total_type(fish) for fish in ['tilapia', 'claria', 'autres'])

#     def total_general_cout(self):
#         """Calcule le coût total général des rations."""
#         return sum(self.total_cout_type(fish) for fish in ['tilapia', 'claria', 'autres'])

#     def __str__(self):
#         return (f"Total général des rations: {self.nb_total_ration}, "
#                 f"Coût total: {self.cout_total_ration}")





 # On crée une classe pour les cycle de Production avec comme attributs : la date et le nom

class AlevinsCycle:
    def __init__(self, data=None):
        # Initialisation dynamique via un dictionnaire
        self.data = data or {
            'tilapia': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'claria': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'autres': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'couts': {
                'tilapia': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'claria': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'autres': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0}
            }, 

            
        }
        # nb = nombre
        self.nb_bassin_ciment = 0
        self.nb_etang_en_terre = 0
        self.nb_bac_hors_sol = 0
        self.nb_cage_rectangulaire = 0
        self.nb_cage_circulaire = 0

        # ct = cout total
        self.ct_bassin_ciment = 0
        self.ct_etang_en_terre = 0
        self.ct_bac_hors_sol = 0
        self.ct_cage_rectangulaire = 0
        self.ct_cage_circulaire = 0

        self.cout_total = 0
        self.nb_total = 0

    
    def calculer_totaux(self):
        self.nb_bassin_ciment = self.nombre_total_infrastructure('bassin_en_ciment')
        self.nb_etang_en_terre = self.nombre_total_infrastructure('etang_en_terre')
        self.nb_bac_hors_sol = self.nombre_total_infrastructure('bac_hors_sol')
        self.nb_cage_rectangulaire = self.nombre_total_infrastructure('cage_rectangulaire')
        self.nb_cage_circulaire = self.nombre_total_infrastructure('cage_circulaire')

        self.ct_bassin_ciment = self.cout_total_infrastructure('bassin_en_ciment')
        self.ct_etang_en_terre = self.cout_total_infrastructure('etang_en_terre')
        self.ct_bac_hors_sol = self.cout_total_infrastructure('bac_hors_sol')
        self.ct_cage_rectangulaire = self.cout_total_infrastructure('cage_rectangulaire')
        self.ct_cage_circulaire = self.cout_total_infrastructure('cage_circulaire')

        self.nb_total = self.total_general()
        self.cout_total = self.total_general_cout()


    def nombre_total_infrastructure(self, infrastructure_type):
        return sum(self.data.get(fish_type, {}).get(infrastructure_type, 0)
                   for fish_type in ['tilapia', 'claria', 'autres'])

    def cout_total_infrastructure(self, infrastructure_type):
        """Calcule le coût total d'achat pour une infrastructure donnée."""
        return sum(self.data['couts'].get(fish_type, {}).get(infrastructure_type, 0)
                   for fish_type in ['tilapia', 'claria', 'autres'])    

    def total_type(self, fish_type):
        """Calcule le total pour un type donné (tilapia, claria, autres)."""
        return sum(self.data[fish_type].values())
    
    def total_cout_type(self, fish_type):
        """Calcule le total des coûts pour un type donné."""
        return sum(self.data['couts'][fish_type].values())
    
    def total_general(self):
        """Calcule le total général de tous les alevins."""
        return sum(self.total_type(fish) for fish in ['tilapia', 'claria', 'autres'])
    
    def total_general_cout(self):
        """Calcule le coût total général."""
        return sum(self.total_cout_type(fish) for fish in ['tilapia', 'claria', 'autres'])

    def __str__(self):
        return f"Total général alevins: {self.total_general()}, Coût total: {self.total_general_cout()}"


class RecolteCycle:
    def __init__(self, data=None):
        # Initialisation dynamique via un dictionnaire
        # infrastructures = {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
        #                 'cage_rectangulaire': 0, 'cage_circulaire': 0}
        
        self.cycle = {
                'tilapia': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                'claria': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                'autres': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                'couts': {
                    'tilapia': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                    'claria': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                    'autres': {
                        'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0
                    },
                }, 
        }

        self.data = data or {
            'vente' : self.cycle,
            'don': self.cycle,
            'autoConsommation': self.cycle
        }

        # nb = nombre
        self.nb_bassin_ciment = 0
        self.nb_etang_en_terre = 0
        self.nb_bac_hors_sol = 0
        self.nb_cage_rectangulaire = 0
        self.nb_cage_circulaire = 0

        # ct = cout total
        self.ct_bassin_ciment = 0
        self.ct_etang_en_terre = 0
        self.ct_bac_hors_sol = 0
        self.ct_cage_rectangulaire = 0
        self.ct_cage_circulaire = 0

        self.cout_total = 0
        self.nb_total = 0 
 
    
    def calculer_totaux(self):
        self.nb_bassin_ciment = self.nombre_total_infrastructure('bassin_en_ciment')
        self.nb_etang_en_terre = self.nombre_total_infrastructure('etang_en_terre')
        self.nb_bac_hors_sol = self.nombre_total_infrastructure('bac_hors_sol')
        self.nb_cage_rectangulaire = self.nombre_total_infrastructure('cage_rectangulaire')
        self.nb_cage_circulaire = self.nombre_total_infrastructure('cage_circulaire')

        self.ct_bassin_ciment = self.cout_total_infrastructure('bassin_en_ciment')
        self.ct_etang_en_terre = self.cout_total_infrastructure('etang_en_terre')
        self.ct_bac_hors_sol = self.cout_total_infrastructure('bac_hors_sol')
        self.ct_cage_rectangulaire = self.cout_total_infrastructure('cage_rectangulaire')
        self.ct_cage_circulaire = self.cout_total_infrastructure('cage_circulaire')

        self.nb_total = self.total_general()
        self.cout_total = self.total_general_cout()


    def nombre_total_infrastructure(self, infrastructure_type):
        total = 0
        for categorie in ['vente', 'don', 'autoConsommation']:
            for fish_type in ['tilapia', 'claria', 'autres']:
                total += self.data[categorie].get(fish_type, {}).get(infrastructure_type, 0)
        return total

    def cout_total_infrastructure(self, infrastructure_type):
        """Calcule le coût total d'achat pour une infrastructure donnée."""
        total = 0
        for categorie in ['vente', 'don', 'autoConsommation']:
            for fish_type in ['tilapia', 'claria', 'autres']:
                total += self.data[categorie]['couts'].get(fish_type, {}).get(infrastructure_type, 0)
        return total    

    def total_type(self, fish_type):
        """Calcule le total pour un type donné (tilapia, claria, autres)."""
        return sum(self.data['vente'][fish_type].values())
    
    def total_cout_type(self, fish_type):
        """Calcule le total des coûts pour un type donné."""
        return sum(self.data['vente']['couts'][fish_type].values())
    
    def total_type_don(self, fish_type):
        """Calcule le total pour un type donné (tilapia, claria, autres)."""
        return sum(self.data['don'][fish_type].values())
    
    def total_cout_type_don(self, fish_type):
        """Calcule le total des coûts pour un type donné."""
        return sum(self.data['don']['couts'][fish_type].values())
    
    def total_type_autoconsommation(self, fish_type):
        """Calcule le total pour un type donné (tilapia, claria, autres)."""
        return sum(self.data['autoConsommation'][fish_type].values())
    
    def total_cout_type_autoconsommation(self, fish_type):
        """Calcule le total des coûts pour un type donné."""
        return sum(self.data['autoConsommation']['couts'][fish_type].values())
    
    
    def total_general(self):
        """Calcule le total général de tous les alevins."""
        return sum(self.total_type(fish) for fish in ['tilapia', 'claria', 'autres'])
    
    def total_general_cout(self):
        """Calcule le coût total général."""
        return sum(self.total_cout_type(fish) for fish in ['tilapia', 'claria', 'autres'])

    def __str__(self):
        return f"Total général alevins: {self.total_general()}, Coût total: {self.total_general_cout()}"



class RationJournaliereCycle:
    def __init__(self, data=None):
        # Initialisation dynamique via un dictionnaire
        self.data = data or {
            'aliment1': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                        'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'aliment2': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'aliment3': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'aliment4': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'aliment5': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},

            'produit1': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'produit2': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},
            'produit3': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                       'cage_rectangulaire': 0, 'cage_circulaire': 0},

            'couts': {
                'aliment1': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'aliment2': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'aliment3': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'aliment4': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'aliment5': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                           'cage_rectangulaire': 0, 'cage_circulaire': 0},

                'produit1': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'produit2': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
                'produit3': {'bassin_en_ciment': 0, 'etang_en_terre': 0, 'bac_hors_sol': 0, 
                            'cage_rectangulaire': 0, 'cage_circulaire': 0},
            }, 
        }
        # nb = nombre par infrastructure (Aliment)
        self.nb_bassin_ciment = 0
        self.nb_etang_en_terre = 0
        self.nb_bac_hors_sol = 0
        self.nb_cage_rectangulaire = 0
        self.nb_cage_circulaire = 0
        # ct = cout total par infrastructure (Aliment)
        self.ct_bassin_ciment = 0
        self.ct_etang_en_terre = 0
        self.ct_bac_hors_sol = 0
        self.ct_cage_rectangulaire = 0
        self.ct_cage_circulaire = 0
        # cout total generale(Aliment)
        self.cout_total = 0
        # nombre total generale(Aliment)
        self.nb_total = 0

        # nb = nombre par infrastructure (Aliment)
        self.nb_bassin_ciment_prod = 0
        self.nb_etang_en_terre_prod = 0
        self.nb_bac_hors_sol_prod = 0
        self.nb_cage_rectangulaire_prod = 0
        self.nb_cage_circulaire_prod = 0
        # ct = cout total par infrastructure (Aliment)
        self.ct_bassin_ciment_prod = 0
        self.ct_etang_en_terre_prod = 0
        self.ct_bac_hors_sol_prod = 0
        self.ct_cage_rectangulaire_prod = 0
        self.ct_cage_circulaire_prod = 0
        # cout total generale(Aliment)
        self.cout_total_prod = 0
        # nombre total generale(Aliment)
        self.nb_total_prod = 0

    
    def calculer_totaux(self):
        # Aliment
        self.nb_bassin_ciment = self.nombre_total_infrastructure('bassin_en_ciment')
        self.nb_etang_en_terre = self.nombre_total_infrastructure('etang_en_terre')
        self.nb_bac_hors_sol = self.nombre_total_infrastructure('bac_hors_sol')
        self.nb_cage_rectangulaire = self.nombre_total_infrastructure('cage_rectangulaire')
        self.nb_cage_circulaire = self.nombre_total_infrastructure('cage_circulaire')

        self.ct_bassin_ciment = self.cout_total_infrastructure('bassin_en_ciment')
        self.ct_etang_en_terre = self.cout_total_infrastructure('etang_en_terre')
        self.ct_bac_hors_sol = self.cout_total_infrastructure('bac_hors_sol')
        self.ct_cage_rectangulaire = self.cout_total_infrastructure('cage_rectangulaire')
        self.ct_cage_circulaire = self.cout_total_infrastructure('cage_circulaire')

        self.nb_total = self.total_general()
        self.cout_total = self.total_general_cout()

        # Produit
        self.nb_bassin_ciment_prod = self.nombre_total_infrastructure_produit('bassin_en_ciment')
        self.nb_etang_en_terre_prod = self.nombre_total_infrastructure_produit('etang_en_terre')
        self.nb_bac_hors_sol_prod = self.nombre_total_infrastructure_produit('bac_hors_sol')
        self.nb_cage_rectangulaire_prod = self.nombre_total_infrastructure_produit('cage_rectangulaire')
        self.nb_cage_circulaire_prod = self.nombre_total_infrastructure_produit('cage_circulaire')

        self.ct_bassin_ciment_prod = self.cout_total_infrastructure_produit('bassin_en_ciment')
        self.ct_etang_en_terre_prod = self.cout_total_infrastructure_produit('etang_en_terre')
        self.ct_bac_hors_sol_prod = self.cout_total_infrastructure_produit('bac_hors_sol')
        self.ct_cage_rectangulaire_prod = self.cout_total_infrastructure_produit('cage_rectangulaire')
        self.ct_cage_circulaire_prod = self.cout_total_infrastructure_produit('cage_circulaire')

        self.nb_total_prod = self.total_general_produit()
        self.cout_total_prod = self.total_general_cout_produit()


    def nombre_total_infrastructure(self, infrastructure_type):
        return sum(self.data.get(aliment, {}).get(infrastructure_type, 0)
                   for aliment in ['aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5'])

    def cout_total_infrastructure(self, infrastructure_type):
        """Calcule le coût total d'achat pour une infrastructure donnée."""
        return sum(self.data['couts'].get(fish_type, {}).get(infrastructure_type, 0)
                   for fish_type in ['aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5'])

    def nombre_total_infrastructure_produit(self, infrastructure_type):
        return sum(self.data.get(aliment, {}).get(infrastructure_type, 0)
                   for aliment in ['produit1', 'produit2', 'produit3'])

    def cout_total_infrastructure_produit(self, infrastructure_type):
        """Calcule le coût total d'achat pour une infrastructure donnée."""
        return sum(self.data['couts'].get(fish_type, {}).get(infrastructure_type, 0)
                   for fish_type in ['produit1', 'produit2', 'produit3'])    

    def total_type(self, fish_type):
        """Calcule le total pour un type donné (tilapia, claria, autres)."""
        return sum(self.data[fish_type].values())
    
    def total_cout_type(self, fish_type):
        """Calcule le total des coûts pour un type donné."""
        return sum(self.data['couts'][fish_type].values())
    
    def total_general(self):
        """Calcule le total général de tous les alevins."""
        return sum(self.total_type(fish) for fish in ['aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5'])
    
    def total_general_cout(self):
        """Calcule le coût total général."""
        return sum(self.total_cout_type(fish) for fish in ['aliment1', 'aliment2', 'aliment3', 'aliment4', 'aliment5'])
    
    def total_general_produit(self):
        """Calcule le total général de tous les alevins."""
        return sum(self.total_type(fish) for fish in ['produit1', 'produit2', 'produit3'])
    
    def total_general_cout_produit(self):
        """Calcule le coût total général."""
        return sum(self.total_cout_type(fish) for fish in ['produit1', 'produit2', 'produit3'])

    def __str__(self):
        return f"Total général alevins: {self.total_general()}, Coût total: {self.total_general_cout()}"



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
    
    # def get_nombre_tilapia_par_type_infrastructure(self, type_infrastructure_nom):
        
    #     return Alevin.objects.filter(
    #         cycleProduction=self,
    #         infrastructure__typeInfrastructure__nom=type_infrastructure_nom
    #     ).aggregate(total_tilapia=Sum('nombreTilapia'))['total_tilapia'] or 0
    

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
    

    def get_total_ration_by_infrastructure(self, field_name, type_infrastructure_nom):
        """
        Récupère la somme d'un champ donné pour une infrastructure spécifique, insensible à la casse et aux espaces,
        pour les rations journalières.

        :param field_name: Nom du champ à agréger (ex : 'quantiteTilapia', 'quantiteClaria')
        :param type_infrastructure_nom: Nom du type d'infrastructure (ex : 'Bassin en ciment')
        :return: Somme des valeurs du champ ou 0 si aucune donnée trouvée
        """
        if not hasattr(RationJournaliere, field_name):
            raise ValueError(f"Le champ '{field_name}' n'existe pas dans le modèle RationJournaliere.")
        
        # Normalisation du type d'infrastructure
        type_infrastructure_nom = type_infrastructure_nom.strip().lower()

        return RationJournaliere.objects.filter(
            cycleProduction=self,
            infrastructure__typeInfrastructure__nom__iexact=type_infrastructure_nom
        ).aggregate(total=Sum(field_name))['total'] or 0
    
    def get_total_recolte_by_infrastructure(self, field_name, type_infrastructure_nom):
        """
        Récupère la somme d'un champ donné pour une infrastructure spécifique, insensible à la casse et aux espaces.
        
        :param field_name: Nom du champ à agréger (ex : 'nombreTilapia', 'nombreClaria')
        :param type_infrastructure_nom: Nom du type d'infrastructure (ex : 'Bassin en ciment')
        :return: Somme des valeurs du champ ou 0 si aucune donnée trouvée
        """
        if not hasattr(Recolte, field_name):
            raise ValueError(f"Le champ '{field_name}' n'existe pas dans le modèle Alevin.")
        
        # Normalisation du type d'infrastructure
        type_infrastructure_nom = type_infrastructure_nom.strip().lower()

        return Recolte.objects.filter(
            cycleProduction=self,
            infrastructure__typeInfrastructure__nom__iexact=type_infrastructure_nom
        ).aggregate(total=Sum(field_name))['total'] or 0
   

    def get_production_summary(self):
        """
        Crée un résumé de la production pour Tilapia, Claria et Autres par type d'infrastructure.
        """
        summary = AlevinsCycle()

        # Définir les types de poissons, infrastructures et types de coût
        poissons = ['tilapia', 'claria', 'autres']
        infrastructures = ['Bassin en ciment', 'Etang en Terre', 'Bac hors sol', 
                            'Cage Rectangulaire', 'Cage Circulaire']
        couts = ['nombre', 'coutAchat']

        # Boucles dynamiques pour remplir les données
        for poisson in poissons:
            for infrastructure in infrastructures:
                # Nombre d'alevins
                count_key = f"{poisson}_{infrastructure.lower().replace(' ', '_')}"
                count_value = self.get_total_alevin_by_infrastructure(f"nombre{poisson.capitalize()}", infrastructure)
                summary.data[poisson][infrastructure.lower().replace(' ', '_')] = count_value

                # Coût associé
                cout_key = f"cout_{poisson}_{infrastructure.lower().replace(' ', '_')}"
                cout_value = self.get_total_alevin_by_infrastructure(f"coutAchat{poisson.capitalize()}", infrastructure)
                summary.data['couts'][poisson][infrastructure.lower().replace(' ', '_')] = cout_value

        return summary
    
    def get_ration_journaliere_summary(self):
        """
        Crée un résumé des rations journalières pour Tilapia, Claria et Autres par type d'infrastructure.
        """
        summary = RationJournaliereCycle()

        # Types de poissons
        #poissons = ['tilapia', 'claria', 'autres']
        infrastructures = ['Bassin en ciment', 'Etang en Terre', 'Bac hors sol', 
                            'Cage Rectangulaire', 'Cage Circulaire']
        
        # Champs pour les aliments et leurs prix
        aliments = [f"aliment{i}" for i in range(1, 6)]  # aliment1 à aliment5
        prix_aliments = [f"prixAliment{i}" for i in range(1, 6)]  # prixAliment1 à prixAliment5

        # Champs pour les produits et leurs prix
        produits = [f"produit{i}" for i in range(1, 4)]  # produit1 à produit3
        prix_produits = [f"prixProduit{i}" for i in range(1, 4)]  # prixProduit1 à prixProduit3

        # Boucles dynamiques pour remplir les données
        for aliment in aliments:
            for infrastructure in infrastructures:
                # Aliment
                count_key = f"{aliment}_{infrastructure.lower().replace(' ', '_')}"
                count_value = self.get_total_ration_by_infrastructure(aliment, infrastructure)
                summary.data[aliment][infrastructure.lower().replace(' ', '_')] = count_value

                # Prix Aliment
                cout_key = f"prix_{aliment}_{infrastructure.lower().replace(' ', '_')}"
                cout_value = self.get_total_ration_by_infrastructure(f"prix{aliment.capitalize()}", infrastructure)
                summary.data['couts'][aliment][infrastructure.lower().replace(' ', '_')] = cout_value

        for produit in produits:
            for infrastructure in infrastructures:
                # Aliment
                count_key = f"{produit}_{infrastructure.lower().replace(' ', '_')}"
                count_value = self.get_total_ration_by_infrastructure(produit, infrastructure)
                summary.data[produit][infrastructure.lower().replace(' ', '_')] = count_value

                # Prix produit
                cout_key = f"prix_{produit}_{infrastructure.lower().replace(' ', '_')}"
                cout_value = self.get_total_ration_by_infrastructure(f"prix{produit.capitalize()}", infrastructure)
                summary.data['couts'][produit][infrastructure.lower().replace(' ', '_')] = cout_value

        return summary


    def get_recolte_summary(self):
        """
        Crée un résumé de la production pour Tilapia, Claria et Autres par type d'infrastructure.
        """
        summary = RecolteCycle()

        # Définir les types de poissons, infrastructures et types de coût
        poissons = ['tilapia', 'claria', 'autres']
        infrastructures = ['Bassin en ciment', 'Etang en Terre', 'Bac hors sol', 
                            'Cage Rectangulaire', 'Cage Circulaire']
        couts = ['nombre', 'coutAchat']
        types = ['vente', 'don', 'autoConsommation']

        # Boucles dynamiques pour remplir les données
        for type in types:
            for poisson in poissons:
                for infrastructure in infrastructures:
                    # Nombre d'alevins
                    count_key = f"{poisson}_{infrastructure.lower().replace(' ', '_')}"
                    
                    if poisson == 'claria':
                        elt = f"poidsTotalVente{poisson.capitalize()}s"
                    else:
                        elt = f"poidsTotalVente{poisson.capitalize()}"
                    #print(f'Yo Recolte Summary: {elt}')

                    count_value = self.get_total_recolte_by_infrastructure(elt, infrastructure)
                    #print(f'Yo count value: {count_value}')
                    summary.data[type][poisson][infrastructure.lower().replace(' ', '_')] = count_value

                    # Coût associé
                    cout_key = f"cout_{poisson}_{infrastructure.lower().replace(' ', '_')}"
                    if poisson == 'claria':
                        elt2 = f"recette{poisson.capitalize()}s"
                    else:
                        elt2 = f"recette{poisson.capitalize()}"
                        
                    cout_value2 = self.get_total_recolte_by_infrastructure(elt2, infrastructure)
                    summary.data[type]['couts'][poisson][infrastructure.lower().replace(' ', '_')] = cout_value2

        return summary    
    
# On crée une classe pour les infrastructures avec comme attributs : type, superficie, volume, numero, dateConstruction, dateReabilitation et natureReabilitation
class Infrastructure(models.Model):
    #ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    typeInfrastructure = models.ForeignKey(TypeInfrastructure, on_delete=models.CASCADE, verbose_name="Type d'Infrastructure")
    numero = models.CharField(max_length=20, blank=True, unique=True)
    superficie = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    dateConstruction = models.DateField(blank=True, null=True)
    dateReabilitation = models.DateField(blank=True, null=True)
    natureReabilitation = models.CharField(max_length=50, blank=True)
    
    # Cette fonction affiche le nom de l'infrastructure
    def __str__(self):
        return f'{self.numero}'

    def save(self, *args, **kwargs):
        if not self.numero:
            prefix = self.typeInfrastructure.code  # Exemple : "CR"
            # On récupère les derniers numéros existants pour ce type
            last_num = (
                Infrastructure.objects
                .filter(typeInfrastructure=self.typeInfrastructure, numero__startswith=prefix)
                .order_by('-numero')
                .first()
            )

            if last_num:
                try:
                    last_index = int(last_num.numero.split('-')[1])
                except (IndexError, ValueError):
                    last_index = 0
            else:
                last_index = 0

            self.numero = f"{prefix}-{last_index + 1}"

        super().save(*args, **kwargs)
    

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

    # # biomasse
    # biomasseTilapia = models.PositiveIntegerField(verbose_name="Biomasse Tilapia", default=0)
    # biomasseClaria = models.PositiveIntegerField(verbose_name="Biomasse Claria", default=0)
    # biomasseAutres = models.PositiveIntegerField(verbose_name="Biomasse Autres", default=0)

    # poids moyen
    poidsMoyenTilapia = models.PositiveIntegerField(verbose_name="Poids Moyen Tilapia", default=0)
    poidsMoyenClaria = models.PositiveIntegerField(verbose_name="Poids Moyen Claria", default=0)
    poidsMoyenAutres = models.PositiveIntegerField(verbose_name="Poids Moyen Autres", default=0)


    @property
    def biomasse_tilapia(self):
        # Valeur Arondi
        return round(((self.nombreTilapia - self.mortaliteTilapia + self.remplaceMortaliteTilapia) * self.poidsMoyenTilapia) / 1000, 2)
        # Valeur Normale(sans arondi)
        #return ((self.nombreTilapia - self.mortaliteTilapia + self.remplaceMortaliteTilapia) * self.poidsMoyenTilapia) / 1000

    @property
    def biomasse_claria(self):
        return round(((self.nombreClaria - self.mortaliteClaria + self.remplaceMortaliteClaria) * self.poidsMoyenClaria) / 1000, 2)

    @property
    def biomasse_autres(self):
        return round(((self.nombreAutres - self.mortaliteAutres + self.remplaceMortaliteAutres) * self.poidsMoyenAutres) / 1000, 2)

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
    prise_poids_tilapia = models.FloatField(verbose_name="Prise Poids Tilapia", default=0)
    prise_poids_claria = models.FloatField(verbose_name="Prise Poids Claria", default=0)
    prise_poids_autres = models.FloatField(verbose_name="Prise Poids Autres", default=0)
    nombreEchantillons = models.PositiveIntegerField(verbose_name="Nombre d'échantillons", default=0)
    nombreTotalPoissonsEchantillonnes = models.PositiveIntegerField(verbose_name="Nbre Total poissons échant.", default=0)
    # poidsTotalEchantillons = models.FloatField(verbose_name="Poids moyen", default=0)
    # poidsMoyen = models.FloatField(verbose_name="Poids Total des echantillons", default=0)
    # prisePoidsTotal = models.FloatField(verbose_name="Prise poids total", default=0)
    # biomasse = models.PositiveIntegerField(verbose_name="Biomasse",default=0)

    # Cette fonction affiche le nom du cycle de production
    # def __str__(self):
    #     return f'{self.nom}'
    

    @property
    def date_de_controle(self):
        if not self.date:
            return datetime.now()
        return self.cycleProduction.date + timedelta(days=30)

    @property
    def nombre_echantilons(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes




    @property
    def poids_total_echant(self):
        # On récupère l'alevin lié au même cycleProduction et infrastructure
        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0

        poids_total = ( self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes) + (alevin.poidsMoyenTilapia * self.nombreTotalPoissonsEchantillonnes)

            
        #print(f'*** biomasse totale : {biomasse_totale * 0.06}')
        #return round(biomasse_totale * 0.06, 2)  # 6% de la biomasse totale
        return round(poids_total, 2)

    @property
    def poids_moyen(self):
        # if self.nombreTotalPoissonsEchantillonnes == 0:
        #     return 0.0
        # return round(self.poidsTotalEchantillons / self.nombreTotalPoissonsEchantillonnes, 2)

        try:
            return round(self.poidsTotalEchantillons / self.nombreTotalPoissonsEchantillonnes, 2)
        except:
            return 0.0

    @property
    def prise_poids_total(self):

        # On récupère l'alevin lié au même cycleProduction et infrastructure
        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0

        if alevin.poidsMoyenTilapia == 0:
            return 0.0

        return round(self.poidsMoyen - alevin.poidsMoyenTilapia, 2)

    @property
    def biomasse_2(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.prise_poids_total * (alevin.nombreTilapia + alevin.nombreClaria + alevin.nombreAutres) / 1000) , 2)


    # Controle 2
    @property
    def date_de_controle_2(self):
        return self.date + timedelta(days=30)

    @property
    def nombre_echantilons_2(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant_2(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes


    @property
    def poids_total_echant_2(self):
        try:
            return (self.prise_poids_tilapia * 30 * self.nombre_total_poisson_echant_2) + (self.poids_moyen * self.nombre_total_poisson_echant_2)
        except:
            return 0.0

    # @property
    # def poidsTotalEchantillons2(self):
    #     if self.prise_poids_tilapia is None or self.poids_moyen is None or self.nombreTotalPoissonsEchantillonnes2 is None:
    #         return 0

    #     return (
    #         self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes2
    #         + self.poids_moyen * self.nombreTotalPoissonsEchantillonnes2
    #     )
    
    @property 
    def poids_moyen_2(self):
        # if (self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2) == None:
        #     return 0.0
        # return self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2
        try:
            return self.poids_total_echant_2 / self.nombre_total_poisson_echant_2
        #except ZeroDivisionError:
        except:
            return 0.0

    @property
    def prise_poids_total_2(self):
        try:
            return self.poids_moyen_2 - self.poids_moyen
        except:
            return 0.0


    

    @property
    def biomasse_3(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.poids_moyen_2 * (alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) / 1000) , 2)


    # Controle 3
    @property
    def date_de_controle_3(self):
        return self.date + timedelta(days=60)

    @property
    def nombre_echantilons_3(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant_3(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes


    @property
    def poids_total_echant_3(self):
        try:
            return (self.prise_poids_tilapia * 60 * self.nombre_total_poisson_echant_3) + (self.poids_moyen_2 * self.nombre_total_poisson_echant_3)
        except:
            return 0.0

    # @property
    # def poidsTotalEchantillons2(self):
    #     if self.prise_poids_tilapia is None or self.poids_moyen is None or self.nombreTotalPoissonsEchantillonnes2 is None:
    #         return 0

    #     return (
    #         self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes2
    #         + self.poids_moyen * self.nombreTotalPoissonsEchantillonnes2
    #     )
    
    @property 
    def poids_moyen_3(self):
        # if (self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2) == None:
        #     return 0.0
        # return self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2
        try:
            return self.poids_total_echant_3 / self.nombre_total_poisson_echant_3
        #except ZeroDivisionError:
        except:
            return 0.0

    @property
    def prise_poids_total_3(self):
        try:
            return self.poids_moyen_3 - self.poids_moyen_2
        except:
            return 0.0

    @property
    def biomasse_4(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.poids_moyen_3 * (alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) / 1000) , 2)
 
    # Controle 4
    @property
    def date_de_controle_4(self):
        return self.date + timedelta(days=90)

    @property
    def nombre_echantilons_4(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant_4(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes

    @property
    def poids_total_echant_4(self):
        try:
            return (self.prise_poids_tilapia * 90 * self.nombre_total_poisson_echant_4) + (self.poids_moyen_3 * self.nombre_total_poisson_echant_4)
        except:
            return 0.0

    # @property
    # def poidsTotalEchantillons2(self):
    #     if self.prise_poids_tilapia is None or self.poids_moyen is None or self.nombreTotalPoissonsEchantillonnes2 is None:
    #         return 0

    #     return (
    #         self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes2
    #         + self.poids_moyen * self.nombreTotalPoissonsEchantillonnes2
    #     )
    
    @property 
    def poids_moyen_4(self):
        # if (self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2) == None:
        #     return 0.0
        # return self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2
        try:
            return self.poids_total_echant_4 / self.nombre_total_poisson_echant_4
        #except ZeroDivisionError:
        except:
            return 0.0

    @property
    def prise_poids_total_4(self):
        try:
            return self.poids_moyen_4 - self.poids_moyen_3
        except:
            return 0.0

    @property
    def biomasse_5(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.poids_moyen_4 * (alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) / 1000) , 2)

    # Controle 5
    @property
    def date_de_controle_5(self):
        return self.date + timedelta(days=120)

    @property
    def nombre_echantilons_5(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant_5(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes

    @property
    def poids_total_echant_5(self):
        try:
            return (self.prise_poids_tilapia * 120 * self.nombre_total_poisson_echant_5) + (self.poids_moyen_4 * self.nombre_total_poisson_echant_5)
        except:
            return 0.0

    # @property
    # def poidsTotalEchantillons2(self):
    #     if self.prise_poids_tilapia is None or self.poids_moyen is None or self.nombreTotalPoissonsEchantillonnes2 is None:
    #         return 0

    #     return (
    #         self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes2
    #         + self.poids_moyen * self.nombreTotalPoissonsEchantillonnes2
    #     )
    
    @property 
    def poids_moyen_5(self):
        # if (self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2) == None:
        #     return 0.0
        # return self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2
        try:
            return self.poids_total_echant_5 / self.nombre_total_poisson_echant_5
        #except ZeroDivisionError:
        except:
            return 0.0

    @property
    def prise_poids_total_5(self):
        try:
            return self.poids_moyen_5 - self.poids_moyen_4
        except:
            return 0.0

    @property
    def biomasse_6(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.poids_moyen_5 * (alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) / 1000) , 2)

    # Controle 6
    @property
    def date_de_controle_6(self):
        return self.date + timedelta(days=150)

    @property
    def nombre_echantilons_6(self):
        return self.nombreEchantillons

    # nombre Total de Poissons Echantillonnes
    @property
    def nbre_total_poisson_echant_6(self):
        #print(f'*** Yo nombreTotalPoissonsEchantillonnes2 {self.nombreTotalPoissonsEchantillonnes}')
        return self.nombreTotalPoissonsEchantillonnes

    @property
    def poids_total_echant_6(self):
        try:
            return (self.prise_poids_tilapia * 150 * self.nombre_total_poisson_echant_6) + (self.poids_moyen_5 * self.nombre_total_poisson_echant_6)
        except:
            return 0.0

    # @property
    # def poidsTotalEchantillons2(self):
    #     if self.prise_poids_tilapia is None or self.poids_moyen is None or self.nombreTotalPoissonsEchantillonnes2 is None:
    #         return 0

    #     return (
    #         self.prise_poids_tilapia * 30 * self.nombreTotalPoissonsEchantillonnes2
    #         + self.poids_moyen * self.nombreTotalPoissonsEchantillonnes2
    #     )
    
    @property 
    def poids_moyen_6(self):
        # if (self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2) == None:
        #     return 0.0
        # return self.poidsTotalEchantillons2 / self.nombreTotalPoissonsEchantillonnes2
        try:
            return self.poids_total_echant_6 / self.nombre_total_poisson_echant_6
        #except ZeroDivisionError:
        except:
            return 0.0

    @property
    def prise_poids_total_6(self):
        try:
            return self.poids_moyen_6 - self.poids_moyen_5
        except:
            return 0.0

    @property
    def biomasse_7(self):

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0


        return round((self.poids_moyen_6 * (alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) / 1000) , 2)


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
    

class Charge(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    eau = models.PositiveIntegerField(verbose_name="Total Eau", default=0)
    main_oeuvre = models.PositiveIntegerField(verbose_name="Total Main d'oeuvre", default=0)
    amortissements = models.PositiveIntegerField(verbose_name="Total Amortissement", default=0)

    # def __str__(self):
    #     return f'{self.nom}'
    def coutTotalCharges(self):
        #return intcomma(self.eau + self.main_oeuvre + self.amortissements)
        return self.eau + self.main_oeuvre + self.amortissements


# class CyclesRation(models.Model):
#     cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
#     infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)
    

# class Ration1(models.Model):
#     cyclesRation = models.ForeignKey(CyclesRation, on_delete=models.CASCADE)
#     date = models.DateField(default=datetime.today)
#     aliment1 = models.FloatField(verbose_name="Aliment 1", default=0)
#     prixAliment1 = models.PositiveIntegerField(verbose_name="Prix Aliment 1", default=0)
#     aliment2 = models.FloatField(verbose_name="Aliment 2", default=0)

# class Ration2(models.Model):
#     cyclesRation = models.ForeignKey(CyclesRation, on_delete=models.CASCADE)
#     date = models.DateField(default=datetime.today)
#     aliment1 = models.FloatField(verbose_name="Aliment 1", default=0)
#     prixAliment1 = models.PositiveIntegerField(verbose_name="Prix Aliment 1", default=0)
#     aliment2 = models.FloatField(verbose_name="Aliment 2", default=0)


    


# On crée une classe pour les ration journalieres avec comme attributs: date, aliment1, aliment2, aliment3, aliment4 (aliment = float)
class RationJournaliere(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)
    #nom = models.CharField(max_length=50, verbose_name="Nom Ration Journalière", blank=True)
    taux_ration_cycle1 = models.FloatField(verbose_name="Taux Ration C1", default=0)
    taux_ration_cycle2 = models.FloatField(verbose_name="Taux Ration C2", default=0)
    taux_ration_cycle3 = models.FloatField(verbose_name="Taux Ration C3", default=0)
    taux_ration_cycle4 = models.FloatField(verbose_name="Taux Ration C4", default=0)
    taux_ration_cycle5 = models.FloatField(verbose_name="Taux Ration C5", default=0)
    taux_ration_cycle6 = models.FloatField(verbose_name="Taux Ration C6", default=0)
    
    prixAliment1 = models.PositiveIntegerField(verbose_name="Prix Aliment1", default=0)
    prixAliment2 = models.PositiveIntegerField(verbose_name="Prix Aliment2", default=0)
    prixAliment3 = models.PositiveIntegerField(verbose_name="Prix Aliment3", default=0)
    prixAliment4 = models.PositiveIntegerField(verbose_name="Prix Aliment4", default=0)
    prixAliment5 = models.PositiveIntegerField(verbose_name="Prix Aliment5", default=0)
    
    prixProduit1 = models.PositiveIntegerField(verbose_name="Prix Produit1", default=0)
    prixProduit2 = models.PositiveIntegerField(verbose_name="Prix Produit2", default=0)
    prixProduit3 = models.PositiveIntegerField(verbose_name="Prix Produit3", default=0)
    
    is_aliment1_cycle1 = models.BooleanField(verbose_name="Aliment1 C1 ?", default=False)
    is_aliment2_cycle1 = models.BooleanField(verbose_name="Aliment2 C1 ?", default=False)
    is_aliment3_cycle1 = models.BooleanField(verbose_name="Aliment3 C1 ?", default=False)
    is_aliment4_cycle1 = models.BooleanField(verbose_name="Aliment4 C1 ?", default=False)
    is_aliment5_cycle1 = models.BooleanField(verbose_name="Aliment5 C1 ?", default=False)
    
    is_produit1_cycle1 = models.BooleanField(verbose_name="Produit1 C1 ?", default=False)
    is_produit2_cycle1 = models.BooleanField(verbose_name="Produit2 C1 ?", default=False)
    is_produit3_cycle1 = models.BooleanField(verbose_name="Produit3 C1 ?", default=False)



    is_aliment1_cycle2 = models.BooleanField(verbose_name="Aliment1 C2 ?", default=False)
    is_aliment2_cycle2 = models.BooleanField(verbose_name="Aliment2 C2 ?", default=False)
    is_aliment3_cycle2 = models.BooleanField(verbose_name="Aliment3 C2 ?", default=False)
    is_aliment4_cycle2 = models.BooleanField(verbose_name="Aliment4 C2 ?", default=False)
    is_aliment5_cycle2 = models.BooleanField(verbose_name="Aliment5 C2 ?", default=False)
    
    is_produit1_cycle2 = models.BooleanField(verbose_name="Produit1 C2 ?", default=False)
    is_produit2_cycle2 = models.BooleanField(verbose_name="Produit2 C2 ?", default=False)
    is_produit3_cycle2 = models.BooleanField(verbose_name="Produit3 C2 ?", default=False)

    is_aliment1_cycle3 = models.BooleanField(verbose_name="Aliment1 C3 ?", default=False)
    is_aliment2_cycle3 = models.BooleanField(verbose_name="Aliment2 C3 ?", default=False)
    is_aliment3_cycle3 = models.BooleanField(verbose_name="Aliment3 C3 ?", default=False)
    is_aliment4_cycle3 = models.BooleanField(verbose_name="Aliment4 C3 ?", default=False)
    is_aliment5_cycle3 = models.BooleanField(verbose_name="Aliment5 C3 ?", default=False)

    is_produit1_cycle3 = models.BooleanField(verbose_name="Produit1 C3 ?", default=False)
    is_produit2_cycle3 = models.BooleanField(verbose_name="Produit2 C3 ?", default=False)
    is_produit3_cycle3 = models.BooleanField(verbose_name="Produit3 C3 ?", default=False)

    is_aliment1_cycle4 = models.BooleanField(verbose_name="Aliment1 C4 ?", default=False)
    is_aliment2_cycle4 = models.BooleanField(verbose_name="Aliment2 C4 ?", default=False)
    is_aliment3_cycle4 = models.BooleanField(verbose_name="Aliment3 C4 ?", default=False)
    is_aliment4_cycle4 = models.BooleanField(verbose_name="Aliment4 C4 ?", default=False)
    is_aliment5_cycle4 = models.BooleanField(verbose_name="Aliment5 C4 ?", default=False)

    is_produit1_cycle4 = models.BooleanField(verbose_name="Produit1 C4 ?", default=False)
    is_produit2_cycle4 = models.BooleanField(verbose_name="Produit2 C4 ?", default=False)
    is_produit3_cycle4 = models.BooleanField(verbose_name="Produit3 C4 ?", default=False)

    is_aliment1_cycle5 = models.BooleanField(verbose_name="Aliment1 C5 ?", default=False)
    is_aliment2_cycle5 = models.BooleanField(verbose_name="Aliment2 C5 ?", default=False)
    is_aliment3_cycle5 = models.BooleanField(verbose_name="Aliment3 C5 ?", default=False)
    is_aliment4_cycle5 = models.BooleanField(verbose_name="Aliment4 C5 ?", default=False)
    is_aliment5_cycle5 = models.BooleanField(verbose_name="Aliment5 C5 ?", default=False)

    is_produit1_cycle5 = models.BooleanField(verbose_name="Produit1 C5 ?", default=False)
    is_produit2_cycle5 = models.BooleanField(verbose_name="Produit2 C5 ?", default=False)
    is_produit3_cycle5 = models.BooleanField(verbose_name="Produit3 C5 ?", default=False)

    is_aliment1_cycle6 = models.BooleanField(verbose_name="Aliment1 C6 ?", default=False)
    is_aliment2_cycle6 = models.BooleanField(verbose_name="Aliment2 C6 ?", default=False)
    is_aliment3_cycle6 = models.BooleanField(verbose_name="Aliment3 C6 ?", default=False)
    is_aliment4_cycle6 = models.BooleanField(verbose_name="Aliment4 C6 ?", default=False)
    is_aliment5_cycle6 = models.BooleanField(verbose_name="Aliment5 C6 ?", default=False)

    is_produit1_cycle6 = models.BooleanField(verbose_name="Produit1 C6 ?", default=False)
    is_produit2_cycle6 = models.BooleanField(verbose_name="Produit2 C6 ?", default=False)
    is_produit3_cycle6 = models.BooleanField(verbose_name="Produit3 C6 ?", default=False)

    
    @property
    def quantite_ration_cycle1(self):
        # On récupère l'alevin lié au même cycleProduction et infrastructure
        print("### Qte ration cycle 1")
        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not alevin:
            return 0.0

        biomasse_totale = (
            alevin.biomasse_tilapia +
            alevin.biomasse_claria +
            alevin.biomasse_autres
        )
        #print(f'*** biomasse totale : {biomasse_totale * 0.06}')
        #return round(biomasse_totale * 0.06, 2)  # 6% de la biomasse totale
        return biomasse_totale * self.taux_ration  

    
    @property
    def quantite_ration_cycle2(self):
        print("### Qte ration cycle 2")
        pecheControle = PecheControle.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        print('### Yo Pêche de controle', pecheControle)
        if not pecheControle:
            return 0.0

        alevin = Alevin.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        print('### Yo Alevin', alevin)
        if not alevin:
            return 0.0
            
        print('### Yo final qte :', ((alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) * pecheControle.poids_moyen) / 1000 * 0.03)
        return  ((alevin.nombreTilapia - alevin.mortaliteTilapia + alevin.remplaceMortaliteTilapia) * pecheControle.poids_moyen) / 1000 * 0.03

    @property
    def quantite_ration_cycle3(self):
        pecheControle = PecheControle.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not pecheControle:
            return 0.0


        return (self.taux_ration_cycle3 * pecheControle.biomasse_3) 

    @property
    def quantite_ration_cycle4(self):
        pecheControle = PecheControle.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not pecheControle:
            return 0.0


        return (self.taux_ration_cycle4 * pecheControle.biomasse_4) 

    @property
    def quantite_ration_cycle5(self):
        pecheControle = PecheControle.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not pecheControle:
            return 0.0


        return (self.taux_ration_cycle5 * pecheControle.biomasse_5) 

    @property
    def quantite_ration_cycle6(self):
        pecheControle = PecheControle.objects.filter(
            cycleProduction=self.cycleProduction,
            infrastructure=self.infrastructure
        ).first()

        if not pecheControle:
            return 0.0


        return (self.taux_ration_cycle6 * pecheControle.biomasse_6) 

    def __str__(self):
        return 'Ration Journalière'
    
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
    recetteTilapia = models.FloatField(verbose_name="Recette Tilapia",default=0, blank=True)
    dateDonTilapia = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonTilapia  = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationTilapia = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationTilapia  = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True)

    # Clarias
    dateVenteClarias = models.DateField(verbose_name="Clarias - Date de vente", default=datetime.today)
    poidsTotalVenteClarias = models.FloatField(verbose_name="Poids total vendu",default=0, blank=True)
    recetteClarias = models.FloatField(verbose_name="Recette Clarias",default=0, blank=True)
    dateDonClarias  = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonClarias   = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationClarias  = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationClarias   = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True) 

    # Autres
    dateVenteAutres = models.DateField(verbose_name="Autres - Date de vente", default=datetime.today)
    poidsTotalVenteAutres = models.FloatField(verbose_name="Poids total vendu",default=0, blank=True)
    recetteAutres = models.FloatField(verbose_name="Recette Autres",default=0, blank=True)
    dateDonAutres = models.DateField(verbose_name="Date de don", default=datetime.today)
    poidsTotalDonAutres = models.FloatField(verbose_name="Poids total donné",default=0, blank=True)
    dateAutoConsommationAutres = models.DateField(verbose_name="Date d'autoconsommation", default=datetime.today)
    poidsTotalAutoConsommationAutres = models.FloatField(verbose_name="Poids total autoconsommation",default=0, blank=True)

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













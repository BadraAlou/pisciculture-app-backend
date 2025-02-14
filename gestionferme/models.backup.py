from django.db import models
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma


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
    

 # On crée une classe pour les cycle de Production avec comme attributs : la date et le nom
class CycleProduction(models.Model):
    date = models.DateField(default=datetime.today, verbose_name="Date de mise en charge")
    nom = models.CharField(max_length=50, blank=True)
    #infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE)

    # Cette fonction affiche le nom du cycle de production
    def __str__(self):
        return f'{self.nom}'
    
    
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



# On crée une classe pour les ration journalieres avec comme attributs: date, aliment1, aliment2, aliment3, aliment4 (aliment = float)
class RationJournaliere(models.Model):
    cycleProduction = models.ForeignKey(CycleProduction, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, blank=True, null=True)

    nom = models.CharField(max_length=50, verbose_name="Nom Ration Journalière", blank=True)
    aliment1 = models.FloatField(verbose_name="Aliment 1", default=0)
    aliment2 = models.FloatField(verbose_name="Aliment 2", default=0)
    aliment3 = models.FloatField(verbose_name="Aliment 3", default=0)
    aliment4 = models.FloatField(verbose_name="Aliment 4", default=0)
    aliment5 = models.FloatField(verbose_name="Aliment 5", default=0)
    produit1 = models.FloatField(verbose_name="Produit 1", default=0, blank=True)
    produit2 = models.FloatField(verbose_name="Produit 2", default=0, blank=True)
    produit3 = models.FloatField(verbose_name="Produit 3", default=0, blank=True)

    # Cette fonction affiche le nom du cycle de production
    def __str__(self):
        return f'{self.nom}'


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


class Dashboard(models.Model):
    nom = models.CharField(max_length=50)

    # Cette fonction affiche le nom et le prenom du pisciculteur
    def __str__(self):
        return f'{self.nom}'


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Infrastructure, Alevin, RationJournaliere, PecheControle, Recolte

@receiver(post_save, sender=Infrastructure)
def create_related_objects(sender, instance, created, **kwargs):
    if created:
        # Création d'un objet Alevin associé
        Alevin.objects.create(
            cycleProduction=instance.cycleProduction,
            infrastructure=instance,
        )
        
        # Création d'un objet RationJournaliere associé
        RationJournaliere.objects.create(
            cycleProduction=instance.cycleProduction,
            infrastructure=instance,
        )
        
        # Création d'un objet PecheControle associé
        PecheControle.objects.create(
            cycleProduction=instance.cycleProduction,
            infrastructure=instance,
        )
        
        # Création d'un objet Recolte associé
        Recolte.objects.create(
            cycleProduction=instance.cycleProduction,
            infrastructure=instance,
        )

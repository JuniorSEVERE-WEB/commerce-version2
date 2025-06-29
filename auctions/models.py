from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle User (hérite de AbstractUser pour pouvoir l'étendre plus tard)
class User(AbstractUser):
    pass

# Modèle pour les annonces d'enchères
class Listing(models.Model):
    title = models.CharField(max_length=100)  # Titre de l'annonce
    description = models.TextField()  # Description détaillée
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Prix initial
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Prix actuel
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)  # Image uploadée
    category = models.CharField(max_length=50, blank=True)  # Catégorie (ex: "Électronique")
    is_active = models.BooleanField(default=True)  # Enchère ouverte/fermée
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")  # Créateur
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")  # Utilisateurs qui surveillent

    def __str__(self):
        return f"{self.title} (${self.current_price})"

# Modèle pour les offres
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Montant de l'offre
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")  # Annonce liée
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")  # Acheteur
    date = models.DateTimeField(auto_now_add=True)  # Date de l'offre

    def __str__(self):
        return f"{self.bidder.username} : ${self.amount} sur {self.listing.title}"

# Modèle pour les commentaires
class Comment(models.Model):
    text = models.TextField()  # Contenu du commentaire
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")  # Annonce liée
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # Auteur
    date = models.DateTimeField(auto_now_add=True)  # Date du commentaire

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.listing.title}"
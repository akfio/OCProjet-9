from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse


class Ticket(models.Model):
    titre = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="projet/static/images/tickets", null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.titre}'

    def get_absolute_url(self):
        return reverse('projet:flux')


RATING_OPTIONS = [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    ]


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], choices=RATING_OPTIONS)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket} ({self.user})' \
               f'{self.rating}' \
               f'{self.headline}' \
               f'{self.body}'

    def get_absolute_url(self):
        return reverse('projet:flux')


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_user')

    class Meta:
        unique_together = ('user', 'followed_user',)
        verbose_name = "Suivi de compte"
        verbose_name_plural = "Suivi de comptes"

    def __str__(self):
        return f'{self.user}'
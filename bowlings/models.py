from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Bowling(models.Model):
    gamer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    score_final = models.IntegerField(
        verbose_name='Score Finale',
        default=0,
        validators=[
            MaxValueValidator(300),
            MinValueValidator(0)
        ]
    )
    is_finished = models.BooleanField(
        default=False,
    )


class Frame(models.Model):
    STATUS = (
        ('Spare', 'Spare'),
        ('Strike', 'Strike'),
        ('Simple', 'Simple'),
    )
    bowling = models.ForeignKey(
        Bowling,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    status = models.CharField(
        max_length=250,
        choices=STATUS
    )
    frame_number = models.PositiveIntegerField(
        verbose_name='Frame Numéro',
    )
    is_done = models.BooleanField(
        default=False
    )


class Lancer(models.Model):
    frame = models.ForeignKey(
        Frame,
        on_delete=models.CASCADE,
        blank=False,
        null=False

    )
    lancer_number = models.PositiveIntegerField(
        verbose_name='Lancer Numéro',
    )
    lancer_score = models.IntegerField(
        verbose_name='Nombre de quilles touchées',
        default=0,
        validators=[
            MaxValueValidator(15),
            MinValueValidator(0)
        ]
    )
    is_additional = models.BooleanField(
        default=False
    )

    # EOF
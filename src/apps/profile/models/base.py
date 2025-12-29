from django.db import models
from apps.core.models.abc import UUID7Model, CreatedUpdatedModel


class NameTypes(models.TextChoices):
    FIRST_NAME = 'first_name', 'first_name'
    LAST_NAME = 'last_name', 'last_name'
    SURNAME = 'surname', 'surname'


class NamesModel(UUID7Model):
    value_type = models.CharField(choices=NameTypes.choices)
    value = models.CharField(max_length=120)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['value_type', 'value'],
                name='unique_type_and_name'
            )
        ]

    def __str__(self):
        return f'{self.value_type}: {self.value}'


class ProfileModel(UUID7Model, CreatedUpdatedModel):
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.slug


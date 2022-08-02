from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    regular_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField()
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name

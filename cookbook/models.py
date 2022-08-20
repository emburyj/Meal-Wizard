from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ingredient(models.Model):
    iid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    ing_type = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    rid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    rec_type = models.CharField(max_length=128)
    source = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cookbook(models.Model):
    rec = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ing = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

class RecipeCollection(models.Model):
    rcid = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class MealPlan(models.Model):
    rec_col = models.ForeignKey(RecipeCollection, on_delete=models.CASCADE)
    rid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
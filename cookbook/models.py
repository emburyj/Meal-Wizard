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

def get_shopping_list(rc):
    mp_query = MealPlan.objects.filter(rec_col__exact=rc)
    ing_dict = {}
    for item in mp_query:
        cb_query = Cookbook.objects.filter(rec__exact=item.rid)
        for foo in cb_query:
            if foo.ing in ing_dict:
                ing_dict[foo.ing] = ing_dict[foo.ing] + foo.qty
            else:
                ing_dict.setdefault(foo.ing, foo.qty)
    return ing_dict


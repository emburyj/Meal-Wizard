from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from cookbook.models import Ingredient, Recipe, Cookbook, RecipeCollection, MealPlan
from cookbook.models import get_shopping_list

# Create your views here.
def home_view(request):
    rec_coll_query = RecipeCollection.objects.all()
    mealplan_recipes = {}
    for item in rec_coll_query:
        rec_query = MealPlan.objects.filter(rec_col__exact=item)
        recs = [mp.rid for mp in rec_query]
        mealplan_recipes.setdefault(item, recs)
    context = {'MP_Recs': mealplan_recipes} # {RecipeCollection_object: [Recipe_object,]}
    return render(request, 'home.html', context)

def create_meal_plan_view(request):
    pass

def meal_plan_detail_view(request, rcid):
    rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
    meal_plan_q = MealPlan.objects.filter(rec_col__exact=rc) # this gives a query obj
    recs = [item.rid for item in meal_plan_q]
    recs_length = range(len(recs))
    recs_ings = {}
    for item in recs:
        recipe_query = Cookbook.objects.filter(rec__exact=item)
        current_ing_dict = {}
        for i in recipe_query:
            current_ing_dict.setdefault(i.ing, i.qty)
        recs_ings.setdefault(item, current_ing_dict) # {recipe_object: {ing_object: qty}}
    context = {'recipes_ingredients': recs_ings, 'rcid': rcid}
    return render(request, 'mp_detail.html', context)

def grocery_list_view(request, rcid):
    rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
    context = {'groceries': get_shopping_list(rc), 'rcid': rcid}
    return render(request, 'grocery_shopping.html', context)

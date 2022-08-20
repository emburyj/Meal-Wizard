from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from cookbook.models import Ingredient, Recipe, Cookbook, RecipeCollection, MealPlan, User
from cookbook.forms import *

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

def create_meal_plan_view(response):
    recs_all_q = Recipe.objects.all() # query of all recipe objects
    recs_all = [x for x in recs_all_q]
    me = User.objects.get(username='josh')
    form = []
    if response.method == "POST":
        new_rc_obj = RecipeCollection(author=me)
        new_rc_obj.save()
        for i in range(0, len(recs_all)):
            if recs_all[i].name in response.POST:
                    new_mp = MealPlan(rec_col=new_rc_obj ,rid=recs_all[i])
                    new_mp.save()
        return HttpResponseRedirect(f"/Meal-Plans/{new_rc_obj.rcid}")
    else:
        for i in range(0, len(recs_all)):
            form.append(new_recipe_collection_form())
            form[i].fields[recs_all[i].name] = form[i].fields["box"]
            del(form[i].fields["box"])
    return render(response, 'create_mp.html', {'form': form})

def meal_plan_detail_view(request, rcid):
    rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
    meal_plan_q = MealPlan.objects.filter(rec_col__exact=rc) # this gives a query obj
    recs = [item.rid for item in meal_plan_q]
    recs_ings = get_recs_ings(recs)
    context = {'recipes_ingredients': recs_ings, 'rcid': rcid}
    return render(request, 'mp_detail.html', context)

def grocery_list_view(request, rcid):
    rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
    context = {'groceries': get_shopping_list(rc), 'rcid': rcid}
    return render(request, 'grocery_shopping.html', context)

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

def get_recs_ings(lst_of_recipes):
    '''
    Desc: This function takes a list of recipes and returns a dict of {Rec_obj: {Ing_obj: qty}}
    '''
    recs_ings = {}
    for item in lst_of_recipes:
        recipe_query = Cookbook.objects.filter(rec__exact=item)
        current_ing_dict = {}
        for i in recipe_query:
            current_ing_dict.setdefault(i.ing, i.qty)
        recs_ings.setdefault(item, current_ing_dict) # {recipe_object: {ing_object: qty}}
    return recs_ings
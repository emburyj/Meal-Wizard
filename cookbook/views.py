from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from cookbook.models import Ingredient, Recipe, Cookbook, RecipeCollection, MealPlan, User
from cookbook.forms import *
from django.utils.dateparse import parse_date
from collections import OrderedDict
from cookbook.forms import rec_type_choices
from cookbook.forms import ing_type_choices
from users.models import *
import random

# --------------------------------------------------------------------------------------#
# Views
# --------------------------------------------------------------------------------------#
@login_required
def home_view(request):
    # all_users_q = User.objects.all()
    # all_users = [x for x in all_users_q]
    current_user = request.user
    recs_all_q = get_recipes_following(current_user).order_by('-created_date')[:10]# query of all recipe objects of current user and everyone they're following; limit to 10
    recs_all_list = [x for x in recs_all_q]
    rec_coll_query = get_recipecollections_following(current_user).order_by('-created_date')[:20] # limit to 20 MP's
    mealplan_recipes = {}
    for item in rec_coll_query:
        rec_query = MealPlan.objects.filter(rec_col__exact=item)
        recs = [mp.rid for mp in rec_query]
        mealplan_recipes.setdefault(item, recs) # mealplan recipes is {RecipeCollection_object: [Recipe_object,]}
    context = {'MP_Recs': mealplan_recipes, 'recent_recipes':recs_all_list}
    return render(request, 'home.html', context)

@login_required
def create_meal_plan_view(response):
    current_user = response.user
    recs_all_q = get_recipes_following(current_user) # query of all recipe objects of current user and everyone they're following
    recs_all = [x for x in recs_all_q]
    recs_ings = get_recs_ings(recs_all)
    prefix = '/cookbook/static/'
    if response.method == "POST":
        start_date = parse_date(response.POST['date'])
        new_rc_obj = RecipeCollection(author=current_user, created_date=start_date)
        new_rc_obj.save()
        if 'wizard_creation' in response.POST.keys():
            user_wizard_recipe = Recipe.objects.get(name=f"{current_user}_wizard_recipe")
            user_wizard_qty = Cookbook.objects.get(rec=user_wizard_recipe)
            num_wizard_mp = user_wizard_qty.qty
            # get some random integers
            if num_wizard_mp > len(recs_all):
                num_wizard_mp = len(recs_all)
            random_indices = []
            for i in range(0, num_wizard_mp):
                while(True):
                    current_rand = random.randrange(0, len(recs_all))
                    if current_rand in random_indices: # no duplicates
                        pass
                    else:
                        random_indices.append(current_rand)
                        break
                current_wizard_recipe = recs_all[random_indices[i]]

                new_mp = MealPlan(rec_col=new_rc_obj ,rid=current_wizard_recipe)
                new_mp.save()
        else:
            for i in range(0, len(recs_all)):
                if recs_all[i].name in response.POST:
                        new_mp = MealPlan(rec_col=new_rc_obj ,rid=recs_all[i])
                        new_mp.save()
        return HttpResponseRedirect(f"/Meal-Plans/{new_rc_obj.rcid}")
    else:
        dateform = new_rc_date_form()
        recs_ings_checkform = {}
        for i in range(0, len(recs_all)):
            checkform = new_recipe_collection_form()
            checkform.fields[recs_all[i].name] = checkform.fields["box"]
            del(checkform.fields["box"])
            recs_ings_checkform[checkform] = recs_ings[recs_all[i]]
    return render(response,
     'create_mp.html',
      {'dateform': dateform,
       'checkform': recs_ings_checkform,
       'admin_media_prefix': prefix})

@login_required
def meal_plan_detail_view(request, rcid):
    if request.method == "POST":
        if 'delete_RC_button' in request.POST.keys():
            rc_to_delete = RecipeCollection.objects.get(rcid=request.POST['delete_RC_button'])
            rc_to_delete.delete()
            return HttpResponseRedirect("/")

    else:
        rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
        meal_plan_q = MealPlan.objects.filter(rec_col__exact=rc) # this gives a query obj
        recs = [item.rid for item in meal_plan_q]
        recs_ings = get_recs_ings(recs)
        context = {'recipes_ingredients': recs_ings, 'recipe_collection': rc}
        return render(request, 'mp_detail.html', context)

@login_required
def grocery_list_view(request, rcid):
    rc = RecipeCollection.objects.get(pk=rcid) # this gives you the RC object
    context = {'groceries': get_shopping_list(rc, request.user.username), 'rcid': rcid}
    return render(request, 'grocery_shopping.html', context)

@login_required
def create_recipe_view(response):
    current_user = response.user

    if response.method == "POST":
        # print(response.POST.dict)
        rec_form = new_recipe_form(response.POST)
        ing_form = new_recipe_ingredients_form(response.POST)
        ing_form.fields[f"ingred0"] = ing_form.fields["ingred"]
        ing_form.fields[f"qty0"] = ing_form.fields["qty"]
        ing_form.fields[f"ing_type0"] = ing_form.fields["ing_type"]
        del(ing_form.fields["ingred"])
        del(ing_form.fields["qty"])
        del(ing_form.fields["ing_type"])
        for i in range(1, 15):
            ing_form.fields[f"ingred{i}"] = ing_form.fields["ingred0"]
            ing_form.fields[f"qty{i}"] = ing_form.fields["qty0"]
            ing_form.fields[f"ing_type{i}"] = ing_form.fields["ing_type0"]


        if rec_form.is_valid() and ing_form.is_valid():
            name = rec_form.cleaned_data["name"]
            rec_type_num = int(rec_form.cleaned_data["rec_type"]) - 1 # tuple for choices starts at 1
            rec_type = list(list(rec_type_choices)[rec_type_num])[1]
            if response.POST["recipe_source_link"]:
                source = response.POST["recipe_source_link"]
            else:
                source = "#"
            new_recipe = Recipe(name=name, rec_type=rec_type, source=source, author=current_user)
            new_recipe.save()

            all_ingredients_query = Ingredient.objects.all()
            all_ingredients = [x.name for x in all_ingredients_query]

            for i in range(0, 15):
                if ing_form.cleaned_data[f"ingred{i}"]:
                    if ing_form.cleaned_data[f"ingred{i}"] in all_ingredients:
                        current_ingredient = Ingredient.objects.get(name=ing_form.cleaned_data[f"ingred{i}"])

                    else:
                        current_ing_type_num = int(ing_form.cleaned_data[f"ing_type{i}"])
                        current_ing_type = list(list(ing_type_choices)[current_ing_type_num])[1]
                        current_ingredient = Ingredient(name=ing_form.cleaned_data[f"ingred{i}"], ing_type=current_ing_type)
                        current_ingredient.save()
                    new_cookbook = Cookbook(rec=new_recipe, ing=current_ingredient, qty=ing_form.cleaned_data[f"qty{i}"])
                    new_cookbook.save()

            return HttpResponseRedirect("/Create-New-Recipe/")
    else:
        recipe_form = new_recipe_form()
        ing_form = {}
        for i in range(0, 15):
            ingredients_form = new_recipe_ingredients_form()
            ingredients_form.fields[f"ingred{i}"] = ingredients_form.fields["ingred"]
            ingredients_form.fields[f"qty{i}"] = ingredients_form.fields["qty"]
            ingredients_form.fields[f"ing_type{i}"] = ingredients_form.fields["ing_type"]
            del(ingredients_form.fields["ingred"])
            del(ingredients_form.fields["qty"])
            del(ingredients_form.fields["ing_type"])
            ing_form.setdefault(i, ingredients_form)
        context = {'recipe_form': recipe_form, 'ingredients_form': ing_form}
        return render(response, 'create_recipe.html', context)


# --------------------------------------------------------------------------------------#
# Helper Functions
# --------------------------------------------------------------------------------------#
def shopping_items(rc):
    '''
    Desc: This function takes a RecipeCollection object and returns a dict of
    {Ingredients_obj: qty} for a cumulative grocery shopping list for the collection.
    '''
    mp_query = MealPlan.objects.filter(rec_col__exact=rc)
    ing_dict = {}
    for item in mp_query:
        cb_query = Cookbook.objects.filter(rec__exact=item.rid)
        for foo in cb_query:
            if foo.ing in ing_dict:
                ing_dict[foo.ing] = ing_dict[foo.ing] + foo.qty
            else:
                ing_dict.setdefault(foo.ing, foo.qty)
    ing_dict = OrderedDict(sorted(ing_dict.items(), key=lambda x: (x[0].ing_type, x[1]), reverse=True))
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

def get_shopping_list(rc, username):
    staple_recipe_name = f"{username}_staple_recipe"
    try:
        staple_recipe = [Recipe.objects.get(name=staple_recipe_name)]
    except:
        staple_recipe = []

    staple_ings = get_recs_ings(staple_recipe)
    shopping = shopping_items(rc)
    if staple_recipe:
        for ing, qty in staple_ings[staple_recipe[0]].items():
            if ing in shopping:
                shopping[ing] = shopping[ing] + qty
            else:
                shopping[ing] = qty
    return shopping

def get_recipes_following(user):

    # get users that user is following
    following_query = Follow.objects.filter(follower=user)
    following_list = [x.followed for x in following_query]
    following_list.append(user) # add user to get their recipes too
    # get recipes authored by these users
    staple_strings = [f"{x.username}_staple_recipe" for x in following_list]
    wizard_strings = [f"{x.username}_wizard_recipe" for x in following_list]
    recipes_following_query = Recipe.objects.filter(author__in=following_list).exclude(name__in=staple_strings)
    recipes_following_query = recipes_following_query.exclude(name__in=wizard_strings)
    return recipes_following_query

def get_recipecollections_following(user):

    # get users that user is following
    following_query = Follow.objects.filter(follower=user)
    following_list = [x.followed for x in following_query]
    following_list.append(user) # add user to get their recipecollections too
    recipecollection_following_query = RecipeCollection.objects.filter(author__in=following_list)

    return recipecollection_following_query
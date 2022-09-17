from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UserRegisterForm, UserFollowForm
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from cookbook.models import *
from users.models import *
from cookbook.forms import new_recipe_ingredients_form, ing_type_choices, rec_type_choices, DeleteButtonForm, WizardRecipe

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! You are now able to log in!")
            josh = User.objects.get(username='josh')
            new_user = User.objects.get(username=username)
            followed_by_josh = Follow(followed=new_user, follower=josh)
            followed_by_josh.save()
            following_josh = Follow(followed=josh, follower=new_user)
            following_josh.save()
            wizard_recipe = Recipe(name=f"{username}_wizard_recipe", rec_type="Other", source="#", author=new_user)
            wizard_recipe.save()
            wizard_ingredient = Ingredient(name=f"{username}_wizard_ingredient",ing_type="Other")
            wizard_ingredient.save()
            wizard_cookbook = Cookbook(rec=wizard_recipe, ing=wizard_ingredient, qty=5)
            wizard_cookbook.save()

            return redirect('login')
        else:
            pass
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request, username):
    displayed_user = User.objects.get(username=username)
    current_user = request.user
    if request.method == "POST":
        # -------------------------------------------------- # # follow form stuff
        if current_user != displayed_user:
            follow_form = UserFollowForm(request.POST)
            if follow_form.is_valid():
                if follow_form.cleaned_data['box']:
                    Follow.objects.get(followed=displayed_user, follower=current_user).delete()
                else:
                    new_follow = Follow(followed=displayed_user, follower=current_user)
                    new_follow.save()
                return HttpResponseRedirect(f"/Profile/{displayed_user.username}")
        # -------------------------------------------------- #  Delete recipe form stuff
        if 'delete_recipe_button' in request.POST.keys():
            rid_delete = request.POST['delete_recipe_button']
            recipe_to_delete = Recipe.objects.get(rid=rid_delete)

            recipe_to_delete.delete()
            return HttpResponseRedirect(f"/Profile/{displayed_user.username}")
        # -------------------------------------------------- #  Wizard recipe creation- recipe qty, implemented as an ingredient.
        if 'wizard_qty_button' in request.POST.keys():
            wizard_recipe_form = WizardRecipe(request.POST)
            if wizard_recipe_form.is_valid():
                if wizard_recipe_form.cleaned_data['qty']:
                    # check if user has set this previously, if so overwrite
                    wizard_recipe = Recipe.objects.get(name=f"{current_user}_wizard_recipe")
                    wizard_ingredient = Ingredient.objects.get(name=f"{current_user}_wizard_ingredient")
                    Cookbook.objects.get(rec=wizard_recipe).delete()
                    Cookbook(rec=wizard_recipe, ing=wizard_ingredient, qty=wizard_recipe_form.cleaned_data['qty']).save()

        # -------------------------------------------------- #  Staple ingredient form stuff
        ing_form = new_recipe_ingredients_form(request.POST)
        ing_form.fields[f"ingred0"] = ing_form.fields["ingred"]
        ing_form.fields[f"qty0"] = ing_form.fields["qty"]
        ing_form.fields[f"ing_type0"] = ing_form.fields["ing_type"]
        del(ing_form.fields["ingred"])
        del(ing_form.fields["qty"])
        del(ing_form.fields["ing_type"])
        for i in range(1, 10):
            ing_form.fields[f"ingred{i}"] = ing_form.fields["ingred0"]
            ing_form.fields[f"qty{i}"] = ing_form.fields["qty0"]
            ing_form.fields[f"ing_type{i}"] = ing_form.fields["ing_type0"]

        staple_recipe_name = f"{username}_staple_recipe"

        # check if staple recipe for this user exists. if so, delete it.
        try:
            staple_check = Recipe.objects.get(name=staple_recipe_name).delete()
        except:
            pass
        staple_recipe = Recipe(name=staple_recipe_name, rec_type='Other', source="#", author=displayed_user)
        staple_recipe.save()

        # query for all ingredients
        all_ingredients_query = Ingredient.objects.all()
        all_ingredients = [x.name for x in all_ingredients_query]

        if ing_form.is_valid():
        # check if ingredient entered already exists. If so, use it. If not, create it. Create cookbook object.
            for i in range(0, 10):
                if ing_form.cleaned_data[f"ingred{i}"]:
                    if ing_form.cleaned_data[f"ingred{i}"] in all_ingredients:
                        current_ingredient = Ingredient.objects.get(name=ing_form.cleaned_data[f"ingred{i}"])

                    else:
                        current_ing_type_num = int(ing_form.cleaned_data[f"ing_type{i}"])
                        current_ing_type = list(list(ing_type_choices)[current_ing_type_num])[1]
                        current_ingredient = Ingredient(name=ing_form.cleaned_data[f"ingred{i}"], ing_type=current_ing_type)
                        current_ingredient.save()
                    new_cookbook = Cookbook(rec=staple_recipe, ing=current_ingredient, qty=ing_form.cleaned_data[f"qty{i}"])
                    new_cookbook.save()
            return HttpResponseRedirect(f"/Profile/{request.user.username}")
        # -------------------------------------------------- #

    else: #get request:
        # follow form stuff
        followers_query = Follow.objects.filter(followed=displayed_user)
        followers_list = [x.follower for x in followers_query]
        following_query = Follow.objects.filter(follower=displayed_user)
        following_list = [x.followed for x in following_query]
        if current_user in followers_list:
            following = True
        else:
            following = False
        follow_form = UserFollowForm()
        follow_form.fields['box'].initial = following

        # date displayed user joined
        date_joined = dt.date(displayed_user.date_joined)
        # all recipes created by displayed user:
        user_recipes = Recipe.objects.filter(author=displayed_user).exclude(name__exact=f"{displayed_user.username}_staple_recipe") # query for al recs by user except staple recipe
        user_recipes = user_recipes.exclude(name__exact=f"{displayed_user.username}_wizard_recipe")
        #delete recipe button forms
        user_recipe_list = [x for x in user_recipes]
        recs_recsdel_form = {}
        for i in range(0, len(user_recipes)):
            del_button = DeleteButtonForm()
            del_button.fields[f'delete_button_{i}'] = del_button.fields['delete_button']
            del(del_button.fields['delete_button'])
            recs_recsdel_form.setdefault(user_recipes[i], del_button) # dict with {recipe: delete form for recipe}

        # form for wizard recipe default
        wizard_qty_form = WizardRecipe()

        # staple ingredient form sutff:
        ing_form = {}
        for i in range(0, 10):
            ingredients_form = new_recipe_ingredients_form()
            ingredients_form.fields[f"ingred{i}"] = ingredients_form.fields["ingred"]
            ingredients_form.fields[f"qty{i}"] = ingredients_form.fields["qty"]
            ingredients_form.fields[f"ing_type{i}"] = ingredients_form.fields["ing_type"]
            del(ingredients_form.fields["ingred"])
            del(ingredients_form.fields["qty"])
            del(ingredients_form.fields["ing_type"])
            ing_form.setdefault(i, ingredients_form)

        context = {'displayed_user': displayed_user, 'date_joined': date_joined,
         'user_recipes_delform': recs_recsdel_form, 'ingredients_form': ing_form,
         'follow': following, 'follow_form': follow_form,
         'followers': followers_list, 'following': following_list,
         'wizard_qty_form': wizard_qty_form,}
         #working on dellete recipes form; probably need to combine user_recipes with del recipe form to traverse over both of these in template
    return render(request, 'users/profile.html', context)
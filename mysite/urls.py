"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from cookbook.views import meal_plan_detail_view, home_view, grocery_list_view, create_meal_plan_view, create_recipe_view
from users import views as user_views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    re_path(r'^Profile/(?P<username>\w+)/$',
            user_views.profile_view,
            name="profile"),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    re_path(r'^$',
        home_view,
        name="home"),
    re_path(r'^Meal-Plans/(?P<rcid>\d+)/$',
        meal_plan_detail_view,
        name="mp_detail"),
    re_path(r'^Grocery-List/(?P<rcid>\d+)/$',
        grocery_list_view,
        name="grocery_shopping"),
    re_path(r'Create-New-Meal-Plan/',
            create_meal_plan_view,
            name="create_mp"),
    re_path(r'Create-New-Recipe/',
            create_recipe_view,
            name="create_recipe"),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # re_path(r'^category/(?P<category_id>\d+)/$',
    #         cat_view,
    #         name="blog_cat")
]

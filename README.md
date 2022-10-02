<p align="center">
    <img src="./cookbook/static/img/mealwizard_logo.png"/>
</p>

# Meal Wizard
**by Josh Embury**

### Overview
Meal Wizard is a website for planning weekly meals, generating shopping lists,
and sharing recipes with other users.
The website can be found at: https://mealwizard.herokuapp.com/

### Motivation
Cooking and eating good food is a large part of my life. At the beginning of
each week, my wife and I spend a significant amount of time planning our meals for
the week. This is done my pulling recipes from a variety of sources,
transcribing the various and sundry ingredients onto a sticky note to serve as a grocery
list, and documenting the recipes so we remember which meals we planned throughout
the week. Over the years we've tried several of the meal delivery services.
However these tend to get expensive after their free trials expire and I don't think the
convenience of the meal prep/delivery that these services provide is worth the additional cost.<br><br>
*Enter the Wizard*<br><br>
The Meal Wizard application has streamlined the weekly meal planning process so we no longer
have to spend our Sunday afternoons being stressed out about what to eat for the week.
By having all of our recipes stored in a single location we can easily select the meals
we want to cook for the week (or have the Meal Wizard randomly select recipes) and generate
our grocery list.
It also allows us to share recipes we've tried with family and friends.

### Features
<ul>
    <li>Secure user accounts</li>
    <li>Create new recipes</li>
    <li>Use The Wizard to generate random weekly meal plan</li>
    <li>Follow other users and share recipes</li>
    <li>Generate grocery shopping list for meal plan</li>
    <li>Customizable user settings</li>
</ul>

### Technologies
<ul>
    <li>Python</li>
    <li>Django</li>
    <li>PostgreSQL</li>
    <li>Heroku</li>
    <li>Bootstrap</li>
</ul>

### Download Instructions

*Ensure that you have installed a Code Editor such as Sublime Text*

METHOD 1, Command Line:

Open terminal and run git clone https://github.com/emburyj/Meal-Wizard.git

METHOD 2, GitHub Web Interface:

1) Visit https://github.com/emburyj/Meal-Wizard
2) Click on the green button labeled Clone or download
3) Select Download ZIP
4) Open the ZIP file and extract its contents to the desired location on your computer
5) Open Sublime Text or the editor of your choice
6) Open a new terminal in your code editor
7) Install all dependencies by running the command "pip install -r requirements.txt"
8) Start the program by typing the command "./manage.py runserver" in your terminal
9) The program will open locally in your browser
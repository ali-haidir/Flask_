from flask import Flask,render_template

#create a flask instance

app = Flask(__name__)

#create a decorator (route)

# @app.route('/')
# def index():
#     return "<h1>Hello world from codemy! </h1>"
@app.route('/')
def index():
    name = "Aimen Wadood"
    stuff = "this is some <strong>Bold</strong> text"
    favorate_pizza = ["peporoni", "saugage", "mushroom", 44]
    return render_template("index.html", name=name, stuff =stuff,favorate_pizza=favorate_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html",
    user_name = name)

# Filters
#safe
#capitalize
#lower
#uper
#title
#trim
#striptags

# create Custom error pages skldks

# 1) invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",),404

#2) Unhandeled Exception
@app.errorhandler(500)
def unhandled_exception(e):
    return render_template("500.html",),500

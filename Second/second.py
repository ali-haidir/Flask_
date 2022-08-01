from flask import Blueprint, render_template

second = Blueprint("second" , __name__, static_folder = "static" , template_folder = "templates")

@second.route("/")
def home():
    return render_template("home.html")

@second.route("/sec")
def sec():
    return "<h1> sec from second  </h1>"

@second.route("/test")
def test():
    return "<h1> test from second </h1>"

#nested
@second.route("/test/test2")
def test2():
    return "<h1> lets try nested routes  </h1>"

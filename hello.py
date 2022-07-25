from flask import Flask,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

#create a flask instance

app = Flask(__name__)
# Add Database
con = 'mysql+mysqlconnector://root:mypass123@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = con
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# engine = create_engine(con)

# my super secret SECRET_KEY
app.config['SECRET_KEY'] = "my super secret key"

# Crreate a Model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name =db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique = True)
    favorate_colour = db.Column(db.String(30))
    date_added = db.Column(db.DateTime,default = datetime.utcnow)

    #create String
    def __repr__(self):
        return '<Name %r>' % self.name


#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("whats your name", validators=[DataRequired()])
    email = StringField("whats your email", validators=[DataRequired()])
    favorate_colour = StringField("whats your favourate colour ")
    submit = SubmitField("Submit")



#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("whats your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a decorator (route)

# @app.route('/')
# def index():
#     return "<h1>Hello world from codemy! </h1>"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    print("somthing happened 2")
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.favorate_colour = request.form['favorate_colour']
        print("somthing happened")
        try:
            db.session.commit()
            flash("USER UPDATED SUCCESSFULLY!!")
            return render_template("update.html", form = form , user_to_update = user_to_update)

        except:
            flash("Error TRY AGAIN!!")
            return render_template("update.html", form = form , user_to_update = user_to_update)

    else:
        return render_template("update.html", form = form , user_to_update = user_to_update)


@app.route('/user/add',methods = ["GET","POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data,email = form.email.data , favorate_colour = form.favorate_colour.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorate_colour.data = ""
        flash("User Added Successfully!! ")
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_users.html",form = form,name = name,our_users = our_users)

@app.route('/')
def index():
    name = "Aimen Wadood"
    stuff = "this is some <strong>Bold</strong> text"
    favorate_pizza = ["peporoni", "saugage", "mushroom", 44]
    flash("welcome to my website!!")
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


#create Name Page
@app.route('/name',methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted Successfully")
    return render_template("name.html",
    name = name,
    form = form)

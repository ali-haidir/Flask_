from flask import Flask,render_template,flash,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user

#referenceing the forms now after shifting them to anouther file
from webforms import *
# from webforms import UserForm,NamerForm,PostForm,PasswordForm,LoginForm,SearchForm


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


# flask login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer ,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
#    author = db.Column(db.String(59))
    date_posted = db.Column(db.DateTime , default = datetime.utcnow)
    slug = db.Column(db.String(255))
    #foreign key to link users (refer to the primary key of the users )
    poster_id = db.Column(db.Integer , db.ForeignKey('users.id'))

# Json Thing ( returning json )
@app.route('/date')
def get_current_date():
    dict = {
    "john" : "peporoni",
    "mery" : "cheeze",
    "ali"  : "mushroom"
    }
    return jsonify(dict)

    # return { "Date": date.today() }

# Crreate a Model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    user_name =db.Column(db.String(30),nullable=False, unique = True)
    name =db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique = True)
    favorate_colour = db.Column(db.String(30))
    date_added = db.Column(db.DateTime,default = datetime.utcnow)

    # do some password stuff
    password_hash = db.Column(db.String(128))
    #user can have many post
    posts = db.relationship('Posts' , backref = 'poster')

    @property
    def password(self):
        raise AttributeError("Password is not a readable artribute!! ")
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def varify_password(self,password):
        return check_password_hash(self.password_hash, password)

    #create String
    def __repr__(self):
        return '<Name %r>' % self.name

#create a decorator (route)

# @app.route('/')
# def index():
#     return "<h1>Hello world from codemy! </h1>"

#add stuff to the navbar
@app.context_processor
def base_file():
    form = SearchForm()
    return dict(form = form )

#create Search function
@app.route('/search' , methods = ['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        #get data from submited form
        post.searched = form.searched.data
        #query the database on the input from searched field
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html' , form = form , searched = post.searched , posts = posts)

# create login page
@app.route('/login', methods = ['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_name = form.user_name.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash , form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("wrong Passowrd, try again  ")
        else:
            flash("user doesnt exits try again ")
    return render_template('login.html' , form = form )


# create logout page
@app.route('/logout' , methods = ['GET' , 'POST'])
@login_required
def logout():
    logout_user()
    flash( " you have been loged out!! Thanks for Stoping by...")
    return redirect(url_for('login'))

# create Dashboard page

@app.route('/dashboard', methods = ['GET' , 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    user_to_update = Users.query.get_or_404(id)
    print("somthing happened 2")
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.favorate_colour = request.form['favorate_colour']
        user_to_update.user_name = request.form['user_name']
        print("somthing happened")
        try:
            db.session.commit()
            flash("USER UPDATED SUCCESSFULLY!!")
            return render_template("dashboard.html", form = form , user_to_update = user_to_update)

        except:
            flash("Error TRY AGAIN!!")
            return render_template("dashboard.html", form = form , user_to_update = user_to_update)

    else:
        return render_template("dashboard.html", form = form , user_to_update = user_to_update, id = id)



    return render_template('dashboard.html'  )


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    user_to_delete_name = user_to_delete.name
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User" +  str(user_to_delete_name) + "deleted SUCCESSFULLY")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_users.html",form = form,name = name,our_users = our_users)
    except:
        flash("whoops There was an error doing this ")



@app.route('/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)

    user_to_update = Users.query.get_or_404(id)
    print("somthing happened 2")
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.favorate_colour = request.form['favorate_colour']
        user_to_update.user_name = request.form['user_name']
        print("somthing happened")
        try:
            db.session.commit()
            flash("USER UPDATED SUCCESSFULLY!!")
            return render_template("update.html", form = form , user_to_update = user_to_update)

        except:
            flash("Error TRY AGAIN!!")
            return render_template("update.html", form = form , user_to_update = user_to_update)

    else:
        return render_template("update.html", form = form , user_to_update = user_to_update, id = id)


@app.route('/user/add',methods = ["GET","POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(user_name = form.user_name.data ,  name = form.name.data ,email = form.email.data , favorate_colour = form.favorate_colour.data , password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorate_colour.data = ""
        form.password_hash.data = ""
        form.user_name.data = ""
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

@app.route('/add-post', methods = ['GET', 'POST'])
# @login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title = form.title.data,poster_id = poster , content = form.content.data  , slug = form.slug.data)
#           clear the form
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''
        # add post data to database
        db.session.add(post)
        db.session.commit()


        flash("Blog post Submitted Successfully")

    #redirecting the webpage
    return render_template("add_post.html" , form = form )

# view all posts
@app.route('/posts')
def posts():
    # Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template('posts.html' , posts = posts)

# view specific post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)


    return render_template('post.html' , post = post)

#edit blog ppost
@app.route('/posts/edit/<int:id>', methods  = ['Get' , 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # update Database
        db.session.add(post)
        db.session.commit()
        flash("post has be updated ")

        return redirect(url_for('post' , id= post.id))
    # print("poster_id = " , post.poster_id)
    # print("id = " , id)
    # print("poster.id = " , post.poster.id)
    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.poster.id
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html' , form = form)
    else:
        flash(" You arnt Autherized to visit this page ")
        return redirect(url_for('posts') )


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if post.poster.id  == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("blog post deleted ")

            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html' , posts = posts)

        except:
            flash("somthing went wrong")
            #grab all the posts from database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html' , posts = posts)
    else:
        flash(" You cannot delete this post ")
        flash("Access Denied ")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html' , posts = posts)


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


#create Name Page
@app.route('/test_pw',methods = ['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ""
        form.password_hash.data = ""
        #flash("Form submitted Successfully")

        #query user on email
        pw_to_check = Users.query.filter_by(email = email).first()

        #check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash , password)



    return render_template("test_pw.html",
    email = email,
    password = password ,
    pw_to_check = pw_to_check,
    passed = passed,
    form = form
    )

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired, EqualTo , Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField



#create a search form
class SearchForm(FlaskForm):
    searched = StringField("searched ", validators=[DataRequired()])
    submit = SubmitField("Submit")




#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("whats your name", validators=[DataRequired()])
    user_name = StringField("Whats your username " , validators = [DataRequired()])
    email = StringField("whats your email", validators=[DataRequired()])
    favorate_colour = StringField("whats your favourate colour ")
    password_hash = PasswordField("password" , validators = [DataRequired() , EqualTo('compare_password', message = 'Password must Match!! ')])
    compare_password = PasswordField('Confirm Password' , validators = [DataRequired()])
    submit = SubmitField("Submit")



#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("whats your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create Postes Form
class PostForm(FlaskForm):
    title = StringField("title ", validators=[DataRequired()])
    #content = StringField("enter content  ", validators=[DataRequired()] , widget = TextArea())
    content = CKEditorField('Enter Content', validators = [DataRequired()])
    author = StringField("whats the author name ")
    slug = StringField("slug ", validators=[DataRequired()])
    submit = SubmitField("submit")


#crate Password form
class PasswordForm(FlaskForm):
    email = StringField("whats your email", validators=[DataRequired()])
    password_hash = PasswordField("whats your password", validators=[DataRequired()])
    submit = SubmitField("Submit ")
#create login Form
class LoginForm(FlaskForm):
    user_name =StringField("Username" , validators = [DataRequired()])
    password = PasswordField("Password" , validators = [DataRequired()])
    submit = SubmitField("Submitt ")

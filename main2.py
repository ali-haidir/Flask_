from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
con = 'mysql+mysqlconnector://root:mypass123@localhost/Persons'
app.config['SQLALCHEMY_DATABASE_URI'] = con


db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='rewards')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward

        load_instance = True


@app.route('/')
def index():
    one_user = User.query.first()
    user_schema = UserSchema()

    output = user_schema.dump(one_user)
    print(output)
    return jsonify({'user': output})


if __name__ == '__main__':
    app.run(debug=True)

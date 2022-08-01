from marshmallow import Schema, fields, post_load, ValidationError, validates, validate


class Person():
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f'{self.name} is {self.age} years old. '


class PersonSchema(Schema):
    name = fields.String(validate=validate.Length(max=5))
    # age = fields.Integer(validate=validate_age)
    age = fields.Integer()
    email = fields.Email()
    location = fields.String(required=False)

    @validates('age')
    def validate_age(self, age):
        if age < 20:
            raise ValidationError("age is to young to be considered !!")

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)


input_data = {}
input_data['name'] = input("Whats your name ??")
input_data['age'] = input("Whats your age ??")
input_data['email'] = input("Whats your email ??")
try:
    schema = PersonSchema()
    person = schema.load(input_data)

    # print(person)

    result = schema.dump(person)
    print(result)

    #person = Person(name=input_data['name'], age=input_data['age'])

    # print(person)

except ValidationError as err:
    print(err)
    print(err.valid_data)

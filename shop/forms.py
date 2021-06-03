from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired, NumberRange
from shop.models import User, PopCategory, Franchise, PopBoxSize
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already Taken. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already Used. Please Use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), ]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=15)])
    address = StringField('Address - First line')
    address_postcode = StringField('Address - Postcode', validators=[Length(max=10)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg'])])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data.lower() != current_user.username.lower():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already Taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already Used. Please Use a different one.')

class CreateProductForm(FlaskForm):
    title = StringField('Title *', validators=[DataRequired(), Length(min=5, max=100)])
    price = FloatField('Add a price (£) - Default is £10.00', default=10.00)
    discount_amount = IntegerField('% of discount - Default is 0%', default=0)
    stock = IntegerField('Stock Amount - Default is 1 item', default=1)
    pop_number = IntegerField('Pop Number - Default is 0', default=0)
    feature_image = FileField('Add a Featured Image (.jpg)', validators=[FileAllowed(['jpg'])])
    prduct_image_1 = FileField('Add a Product Image (.jpg)', validators=[FileAllowed(['jpg'])])
    remove_prduct_image_1 = BooleanField('remove')
    prduct_image_2 = FileField('Add a Product Image (.jpg)', validators=[FileAllowed(['jpg'])])
    remove_prduct_image_2 = BooleanField('remove')
    prduct_image_3 = FileField('Add a Product Image (.jpg)', validators=[FileAllowed(['jpg'])])
    remove_prduct_image_3 = BooleanField('remove')
    prduct_image_4 = FileField('Add a Product Image (.jpg)', validators=[FileAllowed(['jpg'])])
    remove_prduct_image_4 = BooleanField('remove')
    prduct_image_5 = FileField('Add a Product Image (.jpg)', validators=[FileAllowed(['jpg'])])
    remove_prduct_image_5 = BooleanField('remove')
    short_description = TextAreaField('Short Description *', validators=[DataRequired()])
    long_description = TextAreaField('Long Description')
    vaulted = BooleanField('The Pop has been Vaulted')
    is_draft = BooleanField('Draft - (unselect to publish live)', default=1)
    submit = SubmitField('Save Product')

class AddCategoryForm(FlaskForm):
    name = StringField('Name of Category *', validators=[DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Add Category')

    def validate_name(self, name):
        name = PopCategory.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That Category already exits.')

class AddFranchiseForm(FlaskForm):
    name = StringField('Name of Franchise *', validators=[DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Add Franchise')

    def validate_name(self, name):
        name = Franchise.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That Franchise already exits.')

class AddBoxSizeForm(FlaskForm):
    name = StringField('Name of Box Size *', validators=[DataRequired(), Length(min=3, max=15)])
    width = IntegerField('Width of Box (cm)*', validators=[DataRequired(), NumberRange(min=1, max=500, message='Length must be 1-500cm')])
    height = IntegerField('Height of Box (cm)*', validators=[DataRequired(), NumberRange(min=1, max=500, message='Length must be 1-500cm')])
    depth = IntegerField('Depth of Box (cm)*', validators=[DataRequired(), NumberRange(min=1, max=500, message='Length must be 1-500cm')])
    submit = SubmitField('Add Box Size')

    def validate_name(self, name):
        name = PopBoxSize.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That Franchise already exits.')

    def validate_height(self, name):
        name = PopBoxSize.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That Franchise already exits.')

class UpdateCartForm(FlaskForm):
    id = HiddenField('product_id')
    quantity = IntegerField('Quantity', validators=[InputRequired()])

class OrderForm(FlaskForm):
    first_name = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=30, message='First Name must be 2 to 30 characters long')])
    last_name = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=40, message='Last Name must be 2 to 40 characters long')])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    address_first_line = StringField('First Line *', validators=[DataRequired(), Length(min=2, max=100, message='First Line must be 2 to 100 characters long')])
    address_second_line = StringField('Second Line', validators=[Length(max=100, message='Second Line must be upto 100 characters long')])
    address_city = StringField('City', validators=[Length(max=100, message='Country must be upto 100 characters long')])
    address_country = StringField('Country', validators=[Length(max=100, message='Postcode must be upto 100 characters long')])
    address_postcode = StringField('Address - Postcode *', validators=[DataRequired(), Length(min=6, max=10, message='Postcode must be 6 to 10 characters long')])
    remember_address = BooleanField('Remember My Address For Later')
    card_number = IntegerField('Card Number *',validators=[])
    submit = SubmitField('Buy Now')


    def validate_card_number(self, card_number):
        number = str(card_number.data)
        print(len(number))
        if len(number) != 16:
            raise ValidationError('Card number must be 16 digits long')
    
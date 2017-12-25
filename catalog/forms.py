from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
     url, ValidationError

from catalog.models import User


class UserForm(Form):
    firstname = StringField('First Name', validators=[DataRequired(),
                                                      Length(4, 20)])
    lastname = StringField('Last Name', validators=[DataRequired(),
                                                    Length(4, 20)])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(8, 20)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(8, 20)])
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 120), Email()])
    submit = SubmitField('Create')


class CategoryForm(Form):
    title = StringField('Category Name', validators=[DataRequired(),
                                                     Length(4, 50)])
    submit = SubmitField('Create')


class ItemForm(Form):
    title = StringField('Item Name', validators=[DataRequired(),
                                                 Length(4, 50)])
    description = StringField('Item Description', validators=[DataRequired(),
                                                              Length(10, 100)])
    submit = SubmitField()

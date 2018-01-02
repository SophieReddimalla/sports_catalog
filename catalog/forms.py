from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
     url, ValidationError

# Validators for the forms used in the project specified

# Validators for Category form


class CategoryForm(FlaskForm):
    """
    This class defines the validators for the category forms.
    """
    title = StringField('Category Name', validators=[DataRequired(),
                                                     Length(4, 100)])
    submit = SubmitField()

# Validators for Item form


class ItemForm(FlaskForm):
    """
    This class defines the validators for the item forms.
    """
    title = StringField('Item Name', validators=[DataRequired(),
                                                 Length(4, 100)])
    description = StringField('Item Description', validators=[DataRequired(),
                                                              Length(10, 100)])
    submit = SubmitField()

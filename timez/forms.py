from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, ValidationError, \
    TextAreaField, FloatField
from timez.models import Contact


class AddContactForm(FlaskForm):
    contact_name = StringField('Contact name', [validators.DataRequired(),
                               validators.Length(min=2, max=50)])
    platform = StringField('Platform', [validators.DataRequired()])
    comment = TextAreaField('Content', [validators.Optional()])
    location = StringField('Location', [validators.Optional()])
    zone_name = StringField('Zone_name', [validators.Optional()])
    utc_offset = FloatField('Utc_offset', [validators.Optional()])
    submit = SubmitField('Add contact')

    def validate_contact_name(self, contact_name):
        contact = Contact.query.filter_by(contact_name=contact_name.data).first()
        if contact:
            raise ValidationError('That contact_name is taken. Please choose a different one.')


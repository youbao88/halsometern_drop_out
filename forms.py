from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l 
from wtforms import (StringField, SubmitField, BooleanField)
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError
from personnummer import personnummer

def personnummerVerifier(form, field):
    if not personnummer.valid(field.data):
        raise ValidationError(_l('The format of personnummer is not valid'))


class dropout_form(FlaskForm):
    id_code = StringField(_l('Please enter your personal number'), validators = [InputRequired(), Length(6,13), personnummerVerifier, DataRequired()], render_kw={"placeholder": _l("Ten or twelve digits")})
    checked = BooleanField(_l('I consent XXXXXX'), validators =[ InputRequired()])
    submit = SubmitField(_l('Submit'))

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget
from app.models.user import User
from app.models.empresa import Empresa
from app.utils.validators import validar_telefone

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class UserForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    telefone = StringField('Telefone', validators=[DataRequired(), validar_telefone])
    email = StringField('Email', validators=[DataRequired(), Email()])
    empresas = MultiCheckboxField('Empresas', coerce=int)
    submit = SubmitField('Salvar')
    
    def __init__(self, user=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user
        self.empresas.choices = [(e.id, f"{e.razao_social} ({e.tipo_unidade})") 
                                for e in Empresa.query.order_by(Empresa.razao_social).all()]
    
    def validate_email(self, email):
        if self.user is None or self.user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este email já está cadastrado.')

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.empresa import Empresa
from app.utils.validators import validar_cnpj

class EmpresaForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), validar_cnpj])
    razao_social = StringField('Razão Social', validators=[DataRequired(), Length(max=255)])
    nome_fantasia = StringField('Nome Fantasia', validators=[Length(max=255)])
    tipo_unidade = SelectField('Tipo de Unidade', choices=[('Matriz', 'Matriz'), ('Filial', 'Filial')], validators=[DataRequired()])
    logradouro = StringField('Logradouro', validators=[Length(max=255)])
    numero = StringField('Número', validators=[Length(max=10)])
    complemento = StringField('Complemento', validators=[Length(max=100)])
    bairro = StringField('Bairro', validators=[Length(max=100)])
    cep = StringField('CEP', validators=[Length(max=10)])
    municipio = StringField('Município', validators=[Length(max=100)])
    uf = StringField('UF', validators=[Length(max=2)])
    telefone = StringField('Telefone', validators=[Length(max=20)])
    email = StringField('Email', validators=[Length(max=120)])
    submit = SubmitField('Salvar')
    
    def __init__(self, empresa=None, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.empresa = empresa
    
    def validate_cnpj(self, cnpj):
        if self.empresa is None or self.empresa.cnpj != cnpj.data:
            empresa = Empresa.query.filter_by(cnpj=cnpj.data).first()
            if empresa:
                raise ValidationError('Este CNPJ já está cadastrado.')

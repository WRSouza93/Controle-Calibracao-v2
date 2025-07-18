from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.laboratorio import Laboratorio
from app.utils.validators import validar_cnpj

class LaboratorioForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), validar_cnpj])
    razao_social = StringField('Razão Social', validators=[DataRequired(), Length(max=255)])
    nome_fantasia = StringField('Nome Fantasia', validators=[Length(max=255)])
    is_rbc = BooleanField('É RBC (Rede Brasileira de Calibração)')
    numero_cal = StringField('Número CAL (Inmetro)', validators=[Length(max=50)])
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
    
    def __init__(self, laboratorio=None, *args, **kwargs):
        super(LaboratorioForm, self).__init__(*args, **kwargs)
        self.laboratorio = laboratorio
    
    def validate_cnpj(self, cnpj):
        if self.laboratorio is None or self.laboratorio.cnpj != cnpj.data:
            laboratorio = Laboratorio.query.filter_by(cnpj=cnpj.data).first()
            if laboratorio:
                raise ValidationError('Este CNPJ já está cadastrado.')
    
    def validate_numero_cal(self, numero_cal):
        if self.is_rbc.data and not numero_cal.data:
            raise ValidationError('Número CAL é obrigatório para laboratórios RBC.')

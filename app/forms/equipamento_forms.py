from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, FieldList, FormField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models.empresa import Empresa
from app.models.categoria import Categoria

class FaixaUsoForm(FlaskForm):
    valor_minimo = DecimalField('Valor Mínimo', validators=[DataRequired(), NumberRange(min=0)], places=4)
    valor_maximo = DecimalField('Valor Máximo', validators=[DataRequired(), NumberRange(min=0)], places=4)
    
    def validate_valor_maximo(self, valor_maximo):
        if valor_maximo.data <= self.valor_minimo.data:
            raise ValidationError('Valor máximo deve ser maior que o valor mínimo.')

class EquipamentoForm(FlaskForm):
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired(), Length(max=50)])
    nome = StringField('Nome do Equipamento', validators=[DataRequired(), Length(max=100)])
    modelo = StringField('Modelo', validators=[Length(max=100)])
    serie = StringField('Série', validators=[Length(max=100)])
    local_uso = StringField('Local de Uso', validators=[Length(max=255)])
    requer_calibracao = BooleanField('Requer Calibração', default=True)
    faixas_uso = FieldList(FormField(FaixaUsoForm), min_entries=1)
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(EquipamentoForm, self).__init__(*args, **kwargs)
        self.empresa_id.choices = [(e.id, f"{e.razao_social} ({e.tipo_unidade})") 
                                  for e in Empresa.query.order_by(Empresa.razao_social).all()]
        self.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.order_by(Categoria.nome).all()]

import re
from wtforms.validators import ValidationError

def validar_cnpj(form, field):
    """Validador customizado para CNPJ"""
    cnpj = re.sub(r'[^\d]', '', field.data)
    
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve ter 14 dígitos')
    
    # Validação básica de CNPJ
    if cnpj in ['00000000000000', '11111111111111', '22222222222222', '33333333333333',
                '44444444444444', '55555555555555', '66666666666666', '77777777777777',
                '88888888888888', '99999999999999']:
        raise ValidationError('CNPJ inválido')

def validar_telefone(form, field):
    """Validador customizado para telefone"""
    telefone = re.sub(r'[^\d]', '', field.data)
    
    if len(telefone) < 10 or len(telefone) > 11:
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos')

from app import db

# Tabela de associação Many-to-Many entre User e Empresa
user_empresa = db.Table('user_empresa',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('empresa_id', db.Integer, db.ForeignKey('empresas.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=db.func.current_timestamp())
)

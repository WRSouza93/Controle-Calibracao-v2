from app import db

class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    razao_social = db.Column(db.String(255), nullable=False)
    nome_fantasia = db.Column(db.String(255))
    tipo_unidade = db.Column(db.Enum('Matriz', 'Filial'), nullable=False)
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    municipio = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relacionamentos
    users = db.relationship('User', secondary='user_empresa', back_populates='empresas')
    categorias = db.relationship('Categoria', backref='empresa', lazy=True)
    equipamentos = db.relationship('Equipamento', backref='empresa', lazy=True)
    
    def __repr__(self):
        return f'<Empresa {self.razao_social}>'

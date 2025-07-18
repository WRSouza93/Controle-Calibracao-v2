from app import db

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100))
    serie = db.Column(db.String(100))
    local_uso = db.Column(db.String(255))
    requer_calibracao = db.Column(db.Boolean, default=True, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relacionamentos
    faixas_uso = db.relationship('FaixaUso', backref='equipamento', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Equipamento {self.tag} - {self.nome}>'

class FaixaUso(db.Model):
    __tablename__ = 'faixas_uso'
    
    id = db.Column(db.Integer, primary_key=True)
    valor_minimo = db.Column(db.Numeric(10, 4), nullable=False)
    valor_maximo = db.Column(db.Numeric(10, 4), nullable=False)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<FaixaUso {self.valor_minimo} - {self.valor_maximo}>'

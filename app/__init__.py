from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config.development import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar blueprints
    from app.views.auth import auth_bp
    from app.views.user import user_bp
    from app.views.empresa import empresa_bp
    from app.views.laboratorio import laboratorio_bp
    from app.views.categoria import categoria_bp
    from app.views.equipamento import equipamento_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(laboratorio_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(equipamento_bp)
    
    return app

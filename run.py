from app import create_app, db
from app.models.user import User
from app.models.empresa import Empresa
from app.models.laboratorio import Laboratorio
from app.models.categoria import Categoria
from app.models.equipamento import Equipamento, FaixaUso
from app.models.user_empresa import user_empresa

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Função para carregar usuário (necessária para Flask-Login)
from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.forms.categoria_forms import CategoriaForm
from app.models.categoria import Categoria
from app import db

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route('/')
@login_required
def list():
    categorias = Categoria.query.join(Categoria.empresa).order_by(Categoria.nome).all()
    return render_template('categorias/list.html', categorias=categorias)

@categoria_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(
            nome=form.nome.data,
            unidade_medida=form.unidade_medida.data,
            sigla_unidade=form.sigla_unidade.data,
            amplitude_critica=form.amplitude_critica.data,
            empresa_id=form.empresa_id.data
        )
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('categoria.list'))
    return render_template('categorias/create.html', form=form)

@categoria_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)
    
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        categoria.unidade_medida = form.unidade_medida.data
        categoria.sigla_unidade = form.sigla_unidade.data
        categoria.amplitude_critica = form.amplitude_critica.data
        categoria.empresa_id = form.empresa_id.data
        
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('categoria.list'))
    
    return render_template('categorias/edit.html', form=form, categoria=categoria)

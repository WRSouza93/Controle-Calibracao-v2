from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.forms.user_forms import UserForm
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
@login_required
def list():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(nome=form.nome.data, telefone=form.telefone.data, email=form.email.data)
        # Associar empresas selecionadas
        for empresa_id in form.empresas.data:
            empresa = Empresa.query.get(empresa_id)
            if empresa:
                user.empresas.append(empresa)
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('user.list'))
    return render_template('users/create.html', form=form)

@user_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(user=user, obj=user)
    
    if form.validate_on_submit():
        user.nome = form.nome.data
        user.telefone = form.telefone.data
        user.email = form.email.data
        
        # Atualizar empresas associadas
        user.empresas.clear()
        for empresa_id in form.empresas.data:
            empresa = Empresa.query.get(empresa_id)
            if empresa:
                user.empresas.append(empresa)
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('user.list'))
    
    # Pré-selecionar empresas do usuário
    form.empresas.data = [e.id for e in user.empresas]
    return render_template('users/edit.html', form=form, user=user)

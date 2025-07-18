from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required
from app.forms.empresa_forms import EmpresaForm
from app.models.empresa import Empresa
from app.services.cnpj_service import CNPJService
from app import db

empresa_bp = Blueprint('empresa', __name__, url_prefix='/empresas')

@empresa_bp.route('/')
@login_required
def list():
    empresas = Empresa.query.order_by(Empresa.razao_social).all()
    return render_template('empresas/list.html', empresas=empresas)

@empresa_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EmpresaForm()
    if form.validate_on_submit():
        empresa = Empresa(
            cnpj=CNPJService.formatar_cnpj(form.cnpj.data),
            razao_social=form.razao_social.data,
            nome_fantasia=form.nome_fantasia.data,
            tipo_unidade=form.tipo_unidade.data,
            logradouro=form.logradouro.data,
            numero=form.numero.data,
            complemento=form.complemento.data,
            bairro=form.bairro.data,
            cep=form.cep.data,
            municipio=form.municipio.data,
            uf=form.uf.data,
            telefone=form.telefone.data,
            email=form.email.data
        )
        db.session.add(empresa)
        db.session.commit()
        flash('Empresa criada com sucesso!', 'success')
        return redirect(url_for('empresa.list'))
    return render_template('empresas/create.html', form=form)

@empresa_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    empresa = Empresa.query.get_or_404(id)
    form = EmpresaForm(empresa=empresa, obj=empresa)
    
    if form.validate_on_submit():
        empresa.cnpj = CNPJService.formatar_cnpj(form.cnpj.data)
        empresa.razao_social = form.razao_social.data
        empresa.nome_fantasia = form.nome_fantasia.data
        empresa.tipo_unidade = form.tipo_unidade.data
        empresa.logradouro = form.logradouro.data
        empresa.numero = form.numero.data
        empresa.complemento = form.complemento.data
        empresa.bairro = form.bairro.data
        empresa.cep = form.cep.data
        empresa.municipio = form.municipio.data
        empresa.uf = form.uf.data
        empresa.telefone = form.telefone.data
        empresa.email = form.email.data
        
        db.session.commit()
        flash('Empresa atualizada com sucesso!', 'success')
        return redirect(url_for('empresa.list'))
    
    return render_template('empresas/edit.html', form=form, empresa=empresa)

@empresa_bp.route('/api/cnpj/<cnpj>')
@login_required
def buscar_cnpj(cnpj):
    """API endpoint para buscar dados do CNPJ"""
    dados, erro = CNPJService.buscar_dados_cnpj(cnpj)
    
    if erro:
        return jsonify({'error': erro}), 400
    
    return jsonify(dados)

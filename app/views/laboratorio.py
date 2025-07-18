from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.forms.laboratorio_forms import LaboratorioForm
from app.models.laboratorio import Laboratorio
from app.services.cnpj_service import CNPJService
from app import db

laboratorio_bp = Blueprint('laboratorio', __name__, url_prefix='/laboratorios')

@laboratorio_bp.route('/')
@login_required
def list():
    laboratorios = Laboratorio.query.order_by(Laboratorio.razao_social).all()
    return render_template('laboratorios/list.html', laboratorios=laboratorios)

@laboratorio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LaboratorioForm()
    if form.validate_on_submit():
        laboratorio = Laboratorio(
            cnpj=CNPJService.formatar_cnpj(form.cnpj.data),
            razao_social=form.razao_social.data,
            nome_fantasia=form.nome_fantasia.data,
            is_rbc=form.is_rbc.data,
            numero_cal=form.numero_cal.data if form.is_rbc.data else None,
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
        db.session.add(laboratorio)
        db.session.commit()
        flash('Laboratório criado com sucesso!', 'success')
        return redirect(url_for('laboratorio.list'))
    return render_template('laboratorios/create.html', form=form)

@laboratorio_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    laboratorio = Laboratorio.query.get_or_404(id)
    form = LaboratorioForm(laboratorio=laboratorio, obj=laboratorio)
    
    if form.validate_on_submit():
        laboratorio.cnpj = CNPJService.formatar_cnpj(form.cnpj.data)
        laboratorio.razao_social = form.razao_social.data
        laboratorio.nome_fantasia = form.nome_fantasia.data
        laboratorio.is_rbc = form.is_rbc.data
        laboratorio.numero_cal = form.numero_cal.data if form.is_rbc.data else None
        laboratorio.logradouro = form.logradouro.data
        laboratorio.numero = form.numero.data
        laboratorio.complemento = form.complemento.data
        laboratorio.bairro = form.bairro.data
        laboratorio.cep = form.cep.data
        laboratorio.municipio = form.municipio.data
        laboratorio.uf = form.uf.data
        laboratorio.telefone = form.telefone.data
        laboratorio.email = form.email.data
        
        db.session.commit()
        flash('Laboratório atualizado com sucesso!', 'success')
        return redirect(url_for('laboratorio.list'))
    
    return render_template('laboratorios/edit.html', form=form, laboratorio=laboratorio)

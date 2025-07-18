from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.forms.equipamento_forms import EquipamentoForm
from app.models.equipamento import Equipamento, FaixaUso
from app.models.categoria import Categoria
from app import db

equipamento_bp = Blueprint('equipamento', __name__, url_prefix='/equipamentos')

@equipamento_bp.route('/')
@login_required
def list():
    equipamentos = Equipamento.query.join(Equipamento.categoria).join(Equipamento.empresa).order_by(Equipamento.tag).all()
    return render_template('equipamentos/list.html', equipamentos=equipamentos)

@equipamento_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EquipamentoForm()
    if form.validate_on_submit():
        equipamento = Equipamento(
            empresa_id=form.empresa_id.data,
            categoria_id=form.categoria_id.data,
            tag=form.tag.data,
            nome=form.nome.data,
            modelo=form.modelo.data,
            serie=form.serie.data,
            local_uso=form.local_uso.data,
            requer_calibracao=form.requer_calibracao.data
        )
        
        # Adicionar faixas de uso
        for faixa_form in form.faixas_uso.data:
            if faixa_form['valor_minimo'] and faixa_form['valor_maximo']:
                faixa = FaixaUso(
                    valor_minimo=faixa_form['valor_minimo'],
                    valor_maximo=faixa_form['valor_maximo']
                )
                equipamento.faixas_uso.append(faixa)
        
        db.session.add(equipamento)
        db.session.commit()
        flash('Equipamento criado com sucesso!', 'success')
        return redirect(url_for('equipamento.list'))
    return render_template('equipamentos/create.html', form=form)

@equipamento_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    equipamento = Equipamento.query.get_or_404(id)
    form = EquipamentoForm(obj=equipamento)
    
    # Pré-carregar faixas de uso
    while len(form.faixas_uso.entries) < len(equipamento.faixas_uso):
        form.faixas_uso.append_entry()
    
    for i, faixa in enumerate(equipamento.faixas_uso):
        if i < len(form.faixas_uso.entries):
            form.faixas_uso.entries[i].valor_minimo.data = faixa.valor_minimo
            form.faixas_uso.entries[i].valor_maximo.data = faixa.valor_maximo
    
    if form.validate_on_submit():
        equipamento.empresa_id = form.empresa_id.data
        equipamento.categoria_id = form.categoria_id.data
        equipamento.tag = form.tag.data
        equipamento.nome = form.nome.data
        equipamento.modelo = form.modelo.data
        equipamento.serie = form.serie.data
        equipamento.local_uso = form.local_uso.data
        equipamento.requer_calibracao = form.requer_calibracao.data
        
        # Remover faixas existentes
        for faixa in equipamento.faixas_uso:
            db.session.delete(faixa)
        
        # Adicionar novas faixas
        for faixa_form in form.faixas_uso.data:
            if faixa_form['valor_minimo'] and faixa_form['valor_maximo']:
                faixa = FaixaUso(
                    valor_minimo=faixa_form['valor_minimo'],
                    valor_maximo=faixa_form['valor_maximo'],
                    equipamento_id=equipamento.id
                )
                db.session.add(faixa)
        
        db.session.commit()
        flash('Equipamento atualizado com sucesso!', 'success')
        return redirect(url_for('equipamento.list'))
    
    return render_template('equipamentos/edit.html', form=form, equipamento=equipamento)

@equipamento_bp.route('/api/categorias/<int:empresa_id>')
@login_required
def categorias_por_empresa(empresa_id):
    """API endpoint para buscar categorias por empresa"""
    categorias = Categoria.query.filter_by(empresa_id=empresa_id).all()
    return jsonify([{'id': c.id, 'nome': c.nome, 'sigla_unidade': c.sigla_unidade} for c in categorias])

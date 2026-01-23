from flask import Blueprint, render_template, request, redirect, url_for

from models import CompetitionType, db

bp = Blueprint('competition_type', __name__, url_prefix='/admin/competition-type')


@bp.route('/')
def list():
    items = CompetitionType.query.order_by(CompetitionType.name).all()
    return render_template('competition_type/list.html', items=items)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        obj = CompetitionType(
            name=request.form['name'],
            is_active='is_active' in request.form
        )
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('competition_type.list'))

    return render_template('competition_type/form.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    obj = CompetitionType.query.get_or_404(id)

    if request.method == 'POST':
        obj.name = request.form['name']
        obj.is_active = 'is_active' in request.form
        db.session.commit()
        return redirect(url_for('competition_type.list'))

    return render_template('competition_type/form.html', obj=obj)


@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    obj = CompetitionType.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('competition_type.list'))

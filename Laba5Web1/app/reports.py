from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user
from models import db, VisitLog, User  # ← ИСПРАВИЛ ИМПОРТ
from sqlalchemy import func
import csv
from io import StringIO
from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/logs')
@login_required
def logs():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Если пользователь НЕ админ, показываем только его записи
    if current_user.role.name != 'admin':
        logs_query = VisitLog.query.filter_by(user_id=current_user.id).order_by(VisitLog.created_at.desc())
    else:
        logs_query = VisitLog.query.order_by(VisitLog.created_at.desc())
    
    pagination = logs_query.paginate(page=page, per_page=per_page, error_out=False)
    logs = pagination.items
    
    return render_template('logs.html', logs=logs, pagination=pagination)


@reports_bp.route('/pages-stats')
@login_required
def pages_stats():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для доступа к данной странице.', 'error')
        return redirect(url_for('reports.logs'))
    stats = db.session.query(
        VisitLog.path,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()
    
    return render_template('pages_stats.html', stats=stats)

@reports_bp.route('/users-stats')
@login_required
def users_stats():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для доступа к данной странице.', 'error')
        return redirect(url_for('reports.logs'))
    stats = db.session.query(
        VisitLog.user_id,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.user_id).order_by(func.count(VisitLog.id).desc()).all()
    
    # Получаем всех пользователей для отображения ФИО
    users = User.query.all()
    users_dict = {user.id: user for user in users}
    
    return render_template('users_stats.html', stats=stats, users_dict=users_dict)


@reports_bp.route('/export-pages-csv')
@login_required
def export_pages_csv():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для доступа к данной странице.', 'error')
        return redirect(url_for('reports.logs'))
    stats = db.session.query(
        VisitLog.path,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Страница', 'Количество посещений'])
    
    for idx, stat in enumerate(stats, 1):
        writer.writerow([idx, stat.path, stat.count])
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=pages_stats.csv'
    return response

@reports_bp.route('/export-users-csv')
@login_required
def export_users_csv():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для доступа к данной странице.', 'error')
        return redirect(url_for('reports.logs'))
    stats = db.session.query(
        VisitLog.user_id,
        func.count(VisitLog.id).label('count')
    ).group_by(VisitLog.user_id).order_by(func.count(VisitLog.id).desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])
    
    for idx, stat in enumerate(stats, 1):
        user_name = 'Неаутентифицированный пользователь'
        if stat.user_id:
            user = User.query.get(stat.user_id)
            if user:
                user_name = f"{user.surname} {user.firstname} {user.lastname}"
        writer.writerow([idx, user_name, stat.count])
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=users_stats.csv'
    return response
import random
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from faker import Faker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime, timezone
import re
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 
from reports import reports_bp
from sqlalchemy import func
from models import db, Role, User, VisitLog


app = Flask(__name__)
application = app
app.secret_key = "123456789"


app.register_blueprint(reports_bp)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)






from flask import request

@app.before_request
def log_visit():
    # Исключаем логирование статических файлов и самого журнала
    if request.path.startswith('/static'):
        return
    
    # Исключаем логирование самого журнала посещений (чтобы избежать бесконечной записи)
    if request.path.startswith('/logs'):
        return
    
    user_id = current_user.id if current_user.is_authenticated else None
    
    log_entry = VisitLog(
        path=request.path,
        user_id=user_id
    )
    db.session.add(log_entry)
    db.session.commit()


def check_rights(required_permission):
    """
    Декоратор для проверки прав пользователя
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Необходимо авторизоваться', 'error')
                return redirect(url_for('login'))
            
            user_role = current_user.role.name if current_user.role else None
            
            has_permission = False
            
            if user_role == 'admin':
                has_permission = True
            elif user_role == 'user':
                if required_permission in ['can_view_profile', 'can_edit_own_profile', 'can_view_own_logs']:
                    has_permission = True
                elif required_permission == 'can_edit_own_profile':
                    user_id = kwargs.get('user_id')
                    if user_id and current_user.id == user_id:
                        has_permission = True
                elif required_permission == 'can_view_profile':
                    user_id = kwargs.get('user_id')
                    if user_id and current_user.id == user_id:
                        has_permission = True
            
            if not has_permission:
                flash('У вас недостаточно прав для доступа к данной странице.', 'error')
                return redirect(url_for('index'))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator






with app.app_context():
    db.create_all()
    # Создаем роли, если их нет
    roles = [
        Role(name='admin', description='Полный доступ ко всем функциям системы'),
        Role(name='moderator', description='Управление пользователями, но без прав администратора'),
        Role(name='user', description='Обычный пользователь, только просмотр и редактирование своего профиля')
    ]
    
    for role_data in roles:
        existing = Role.query.filter_by(name=role_data.name).first()
        if not existing:
            db.session.add(role_data)
    
    db.session.commit()

    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role and not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            firstname='Admin',
            surname='Admin',
            lastname='Admin',
            role_id=admin_role.id
        )
        db.session.add(admin)
        db.session.commit()
        print("Админ создан: login=admin, password=admin123")





def validate_password(password):
    errors = []
    
    # Проверка длины
    if len(password) < 8:
        errors.append('Пароль должен быть не менее 8 символов')
    if len(password) > 128:
        errors.append('Пароль должен быть не более 128 символов')
    
    # Проверка на пробелы
    if ' ' in password:
        errors.append('Пароль не должен содержать пробелов') 
    
    # Проверка на допустимые символы
    allowed_chars = r'^[a-zA-Zа-яА-ЯёЁ0-9~!?@#$%^&*_\-+()\[\]{}></\\|"\'.:,;]+$'
    if not re.match(allowed_chars, password):
        errors.append('Пароль содержит недопустимые символы')
    
    # Проверка на наличие хотя бы одной заглавной латинской или кириллической буквы
    if not re.search(r'[A-ZА-ЯЁ]', password):
        errors.append('Пароль должен содержать хотя бы одну заглавную букву')
    
    # Проверка на наличие хотя бы одной строчной латинской или кириллической буквы
    if not re.search(r'[a-zа-яё]', password):
        errors.append('Пароль должен содержать хотя бы одну строчную букву')
    
    # Проверка на наличие хотя бы одной цифры
    if not re.search(r'[0-9]', password):
        errors.append('Пароль должен содержать хотя бы одну цифру')
    
    return errors



@app.route('/')
def index():
    return render_template('index.html')





@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        user_pass = request.form.get('password')
        user = User.query.filter_by(username=user_name).first()
        if user and check_password_hash(user.password_hash, user_pass):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('reg'))
    return render_template('login.html')

      


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


    

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        user_name = request.form.get('username')
        user_pass = request.form.get('password')
        user_firstname = request.form.get('firstname')
        user_surname = request.form.get('surname')
        user_lastname = request.form.get('lastname')
        
        errors = {}
        
        # Проверка логина
        if not user_name:
            errors['username'] = 'Логин обязателен'
        elif not re.match("^[a-zA-Z0-9]{5,}$", user_name):
            errors['username'] = 'Логин должен содержать только латинские буквы и цифры, минимум 5 символов'
        
        # Проверка пароля
        password_errors = validate_password(user_pass)
        if password_errors:
            errors['password'] = password_errors
        
        # Проверка остальных полей
        if not user_firstname:
            errors['firstname'] = 'Имя обязательно'
        if not user_surname:
            errors['surname'] = 'Фамилия обязательна'
        if not user_lastname:
            errors['lastname'] = 'Отчество обязательно'
        
        # Проверка существующего пользователя
        existing_user = User.query.filter_by(username=user_name).first()
        if existing_user:
            errors['username'] = 'Пользователь с таким ником уже существует'
        
        if errors:
            return render_template('register.html', 
                                 form_data=request.form,
                                 errors=errors)
        
        # Находим роль "user"
        user_role = Role.query.filter_by(name='user').first()
        
        hashed = generate_password_hash(user_pass)
        
        # Создаем пользователя с ролью user
        new_user = User(
            username=user_name,
            password_hash=hashed,
            firstname=user_firstname,
            surname=user_surname,
            lastname=user_lastname,
            role_id=user_role.id  # автоматически ставим роль user
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    
    # GET запрос - показываем пустую форму
    return render_template('register.html', form_data={}, errors={})


@app.route('/corrections', methods=['GET', 'POST'])
@login_required
def correct():
    # Если пользователь не админ, показываем только его
    if current_user.role.name != 'admin':
        users = [current_user]  # только себя
    else:
        users = User.query.all()
    
    for user in users:
        print(f"User: {user.username}, created_at: {user.created_at}")
    return render_template('corrections.html', users=users)

@login_required
@app.route('/user/<int:user_id>')
@check_rights('can_view_profile')
def user_ak(user_id):
    # Обычный пользователь может смотреть только свой профиль
    if current_user.role.name != 'admin' and current_user.id != user_id:
        flash('Вы можете просматривать только свой профиль', 'error')
        return redirect(url_for('correct'))
    
    user = User.query.get(user_id)
    roles = Role.query.all()
    return render_template('user.html', user=user, roles=roles)

@login_required
@app.route('/editing/<int:user_id>', methods=['POST', 'GET'])
@check_rights('can_edit_own_profile')
def edit(user_id):
    # Обычный пользователь может редактировать только себя
    if current_user.role.name != 'admin' and current_user.id != user_id:
        flash('Вы можете редактировать только свой профиль', 'error')
        return redirect(url_for('correct'))
    
    user = User.query.get(user_id)
    roles = Role.query.all()
    
    if request.method == 'GET':
        return render_template('editing.html', user=user, roles=roles)
    else:
        user_firstname = request.form.get('firstname')
        user_surname = request.form.get('surname')
        user_lastname = request.form.get('lastname')
        role_id = request.form.get('role_id')

        if user_surname:
            user.surname = user_surname
        if user_firstname:
            user.firstname = user_firstname
        if user_lastname:
            user.lastname = user_lastname
        
        # Только админ может менять роль
        if current_user.role.name == 'admin' and role_id:
            user.role_id = role_id
        
        db.session.commit()
        flash('Данные успешно обновлены', 'success')
        return redirect(url_for('correct'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@check_rights('can_delete_user')
def delete_user(user_id):
    # Нельзя удалить себя
    if current_user.id == user_id:
        flash('Вы не можете удалить свой аккаунт', 'error')
        return redirect(url_for('correct'))
    
    user = User.query.get(user_id)
    if user:
        full_name = f"{user.surname} {user.firstname} {user.lastname}"
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь {full_name} успешно удален', 'success')
    return redirect(url_for('correct'))


@app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    if current_user.id != user_id:
        flash('У вас нет прав для смены пароля другого пользователя', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        errors = {}
        
        # Проверяем старый пароль
        if not check_password_hash(user.password_hash, old_password):
            errors['old_password'] = 'Неверный текущий пароль'
        
        # Проверяем новый пароль
        if not new_password:
            errors['new_password'] = 'Новый пароль не может быть пустым'
        elif new_password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'
        elif len(new_password) < 8:
            errors['new_password'] = 'Пароль должен быть не менее 8 символов'
        
        # Если ошибок нет - меняем пароль
        if not errors:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Пароль успешно изменен', 'success')
            return redirect(url_for('index'))
        
        return render_template('change_password.html', 
                               user=user,
                               form_data=request.form,
                               errors=errors)
    
    return render_template('change_password.html', user=user, form_data={}, errors={})


if __name__ == '__main__':
    app.run()   
import random
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from faker import Faker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import UserMixin

fake = Faker()

app = Flask(__name__)
application = app
app.secret_key = "123456789"
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin):
    def __init__(self, username):
        self.id = username  # ОБЯЗАТЕЛЬНО! Flask-Login использует id
        self.username = username



def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments(replies=True)
    }

def check_num(n):
        if n[0] + n[1] == '+7':
            num = n.replace(' ','').replace('-', '').replace('(','').replace(')','').replace('.', '')
            for i in range(1, len(num)):
                if num[i] not in '0123456789':
                    return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            if len(num) == 12:
                num = "8" + num[2:]
                num = num[0] + '.' + num[1:4] + '.' + num[4:7] + '.' + num[7:9] + '.' + num[9:]
            else:
                return "Недопустимый ввод. Неверное количество цифр."
        elif n[0] == '8':
            num = n.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '')
            for i in range(len(num)):
                if num[i] not in '0123456789':
                    return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            if len(num) == 11:
                num = num[0] + '.' + num[1:4] + '.' + num[4:7] + '.' + num[7:9] + '.' + num[9:]
            else:
                return "Недопустимый ввод. Неверное количество цифр."
        else:
            num = n.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '')
            for i in range(len(num)):
                if num[i] not in '0123456789':
                    return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            if len(num) == 10:
                num =  '8.' + num[0:3] + '.' + num[3:6] + '.' + num[6:8] + '.' + num[8:]
            else:
                return "Недопустимый ввод. Неверное количество цифр."
        return num

posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/visits')
def visits():
    session['visit'] = session.get('visit', 0) + 1

    return render_template('visits.html', visit = session['visit'])

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login вызывает эту функцию, чтобы получить пользователя по id
    return User(user_id)  # Создаем и возвращаем пользователя

@app.route('/login', methods=['GET', 'POST'])
def login():
    users_in = [
        ('user', 'qwerty')
     ]
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        if (user_name, password) in users_in:
            user = User(user_name)
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page :
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            return 'Неверный логин или пароль'

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

@app.route('/secret', methods = ['GET', 'POST'])

def secret():
    if current_user.is_authenticated:
        return render_template('secret.html')
    else:
        return render_template('login.html', message = 'Для доступа войдите в систему', next = request.url)
    
    



if __name__ == '__main__':
    app.run()   
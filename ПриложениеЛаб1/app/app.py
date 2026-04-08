import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from faker import Faker


fake = Faker()

app = Flask(__name__)
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

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

@app.route('/form', methods = ['GET', 'POST'])
def form():
    form_data = None
    if request.method == "POST":
        form_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'message': request.form.get('message')
        }
    
    return  render_template('form.html', form_data=form_data)

@app.route('/number', methods=['GET', 'POST'])
def number():
    result = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone:  
            result = check_num(phone)
        else:
            result = "Введите номер телефона"
    



    return render_template('number.html',result = result)

@app.route('/url', methods=['GET', 'POST'])
def url():
    request_url = {
        'url_params': dict(request.args)
    }
    return render_template('url.html', request_url = request_url)

@app.route('/myheader', methods=['GET', 'POST'])
def myheader():
    request_header = {
        'header': dict(request.headers)
    }
    return render_template('myheader.html', request_header = request_header)


@app.route('/mycookie', methods=['GET', 'POST'])
def mycookie():
    if request.method == 'POST':
        # Если нажали кнопку - устанавливаем cookies
        response = make_response(redirect (url_for('mycookie')))
        response.set_cookie('username', 'Артём', max_age=60*60*24*30)
        response.set_cookie('lastname', 'Васильев', max_age=60*60*24*30)
        response.set_cookie('language', 'ru', max_age=60*60*24*30),
        response.set_cookie('country', 'Россия', max_age=60*60*24*30)
        return response
    
    # GET запрос - просто показываем страницу с текущими cookies
    all_cookies = dict(request.cookies)
    return render_template('mycookie.html', cookies=all_cookies)



if __name__ == '__main__':
    app.run()   
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        (5, 'отлично'),
        (4, 'хорошо'),
        (3, 'удовлетворительно'),
        (2, 'неудовлетворительно'),
        (1, 'плохо'),
        (0, 'ужасно')
    ], coerce=int, default=5)
    text = TextAreaField('Текст отзыва', validators=[DataRequired()])
    submit = SubmitField('Отправить отзыв')
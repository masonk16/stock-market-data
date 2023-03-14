import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap5(app)


class Form(FlaskForm):
    """
    Form to get data for requesting stock data.
    """
    symbol = StringField('symbol')
    date = StringField('date', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

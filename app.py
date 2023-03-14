import os
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

bootstrap = Bootstrap5(app)

API_ACCESS_KEY = os.getenv("API_ACCESS_KEY")


class MyForm(FlaskForm):
    """
    Form to get data for requesting stock data.
    """

    symbol = StringField("Symbol", validators=[DataRequired()])
    date_from = DateField("From", format="%Y-%m-%d")
    date_to = DateField("To", format="%Y-%m-%d")


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()
    if request.method == "POST":
        # if form.validate_on_submit():
        symbol = form.symbol.data
        date_from = form.date_from.data
        date_to = form.date_to.data
        return redirect(f"/stock_data/{symbol}/{date_from}/{date_to}")

    return render_template("index.html", form=form)


@app.route("/stock_data/<symbol>/<date_from>/<date_to>")
def stock_data(symbol, date_from, date_to):
    response = requests.get(
        f"http://api.marketstack.com/v1/eod?access_key={API_ACCESS_KEY}&symbols={symbol}&date_from={date_from}&date_to={date_to}"
    )
    data = response.json()["data"]
    return render_template("data.html", symbol=symbol, data=data)


if __name__ == "__main__":
    app.run(debug=True)

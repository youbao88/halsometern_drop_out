from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import dropout_form
from flask_bootstrap import Bootstrap5
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_babel import Babel, _
from config import Config
from personnummer import personnummer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap5(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "60 per hour"],
    storage_uri="memory://",
)

def get_locale():
    language = session.get('language')
    if language is not None:
        return language 
    else:
        session['language'] = 'sv'
        return 'sv'
babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def utility_processor():
    return dict(lang=get_locale())

db = SQLAlchemy(app)

class DroppedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idCode = db.Column(db.String(100), nullable=False)
    timeStamp = db.Column(db.DateTime(timezone = True), server_default = func.now())
class InvitedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idCode = db.Column(db.String(100), nullable=False)


@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(request.referrer)

@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"], error_message=_("You have vistied our page too quickly, please wait one minute."))
def home():
    form = dropout_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            personal_number = personnummer.Personnummer(request.form.get('id_code'))
            id_code = str(personal_number.format(True))
            if InvitedUsers.query.filter_by(idCode = id_code).first():
                #Check if id_code already exists
                if  DroppedUsers.query.filter_by(idCode = id_code).first() is None:
                    DroppedUser = DroppedUsers(idCode = id_code)
                    db.session.add(DroppedUser)
                    db.session.commit()
                session['id_code'] = id_code
                return redirect(url_for('thankyou'))
            else:
                flash(_('Invalid ID'), 'error')
    return render_template('home.html', form = form)

@app.route("/thankyou", methods=["GET", "POST"])
def thankyou():
    print(session.get('id_code'))
    if session.get('id_code'):
        return render_template('thankyou.html')
    else:
        flash(_('You are not allowed to visit this page, redirected to the home page'))
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
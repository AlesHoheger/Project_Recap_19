from flask import Flask, render_template, request, make_response
import random
from models import db, User
import sqlalchemy

USER_EMAIL_COOKIE_NAME = 'user_email'
MAX_NUMBER = 10

app = Flask(__name__)
db.create_all()


def get_user_from_cookie():
    email_from_cookie = request.cookies.get(USER_EMAIL_COOKIE_NAME)
    return db.query(User).filter_by(email=email_from_cookie).first()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.cookies.get(USER_EMAIL_COOKIE_NAME) is None:
        response = make_response(render_template('index.html', title='Dobrodošel!'))
    else:
        user = get_user_from_cookie()
        response = make_response(render_template('index.html', title='Vso srečo!', user=user, max_guess=MAX_NUMBER))
    return response


@app.route('/add-user', methods=['POST'])
def add_user():
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    first_secret_number = random.randint(1, MAX_NUMBER)
    new_user = User(name=user_name, email=user_email, secret_number=first_secret_number)

    db.add(new_user)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        m = 'Napaka pri dodajanju uporabnika!'
        return make_response(render_template('generic_message.html', message=m, type='danger'))
    else:
        m = 'Uspešno dodan uporabnik!'
        response = make_response(render_template('generic_message.html', message=m, type='success'))
        response.set_cookie(USER_EMAIL_COOKIE_NAME, user_email)
        return response


@app.route('/result', methods=['POST'])
def result():
    guess = int(request.form.get('guess'))

    user = get_user_from_cookie()
    secret_number = user.secret_number

    if guess == secret_number:
        # create new secret number for the next game
        user.secret_number = random.randint(1, MAX_NUMBER)
        db.add(user)
        db.commit()
        message = "Pravilno! Skrito število je {0}. ".format(str(secret_number)) + \
                  "Za novo igro se vrni na začetno stran"
        return make_response(render_template("generic_message.html", title='Bravo!', message=message, type='success'))
    elif guess > secret_number:
        message = "Tvoj poizkus ni pravilen. Poizkusi z manjšim številom."
        return render_template("generic_message.html", title='Narobe!', message=message)
    elif guess < secret_number:
        message = "Tvoj poizkus ni pravilen. Poizkusi z večjim številom."
        return render_template("generic_message.html", title='Narobe!', message=message)


if __name__ == '__main__':
    app.run()

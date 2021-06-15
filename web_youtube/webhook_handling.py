from flask import Flask, request, redirect, render_template, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.secret_key = 'fkpasdfk32425o23pkfpk23f'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('login'))
        elif 'logout' in request.form:
            return redirect(url_for('logout'))
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/view')
def view():
    return render_template("view.html", values=users.query.all())


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session['email'] = found_user.email
        else:
            usr= users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!", "info")
        return redirect(url_for('user'))
    else:
        if "user" in session: # if already logged in
            flash("Already logged in!", "info")
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if 'user' in session:
        user=session['user']
        if request.method == "POST":
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Your email is successfully registered!", "info")
        else:
            if "email" in session:
                email = session['email']
        return render_template("user.html", email=email, user=user)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f'You are successfully logged out, {user}. You can safely close the browser.', category='info')
    session.pop("user", None) # remove user data from the session. None is a message associated with the data.
    return redirect(url_for('login'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

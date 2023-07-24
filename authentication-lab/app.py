from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebaseConfig = {
  "apiKey": "AIzaSyCPYfxpikpJSfkYxcV1Konz9-n5Y-s_umA",
  "authDomain": "myfirebaseapp-meet.firebaseapp.com",
  "projectId": "myfirebaseapp-meet",
  "storageBucket": "myfirebaseapp-meet.appspot.com",
  "messagingSenderId": "149651312873",
  "appId": "1:149651312873:web:f41c78579cdd16bad06078",
  "measurementId": "G-9BXGJFTCKN",
  "databaseURL" : "https://myfirebaseapp-meet-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()



@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email , password)

            return redirect(url_for("add_tweet"))
        except:
            return render_template("signin.html")

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            userid = login_session['user']['localId']
            user = {
                "email" : email,
                "fullname" : request.form['fullname'],
                "username" : request.form['username'],
                "bio" : request.form['bio']
            }
            db.child("Users").child(userid).set(user)
            return redirect(url_for("add_tweet"))
        except:
            return render_template("signup.html")
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = {
            "title" : request.form['title'],
            "text" : request.form['text'],
            "userid" : login_session['user']['localId']


        }
    return render_template("add_tweet.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
@app.route('/signout', methods=['POST' , 'GET'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for("signin"))


if __name__ == '__main__':
    app.run(debug=True)
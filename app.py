from flask import *
import os
import sqlite3
from sqlite3 import Error

from passlib.context import CryptContext
import getpass

from userlogin import UserLogin

app = Flask(__name__)

app.secret_key = 'aaaaaeeee'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
  return render_template('index.html')


@app.route("/home")

def home():
  return render_template("home.html")

@app.route("/home",  methods=['GET', 'POST'])
def return_text():
  username = request.form['username']
  password = request.form['password']
  ret_user = UserLogin(username,password)
  ret_user_status = ret_user.check_user_exists(username)
  if(ret_user_status == False):
      flash('Something')
      return redirect(url_for('home'))
  else:
    ret_user_pass = ret_user.check_password(username, password)
    if(ret_user_pass == False):
      flash('Invalid Password')
      return redirect(url_for('home'))
    else:
      return('Logged in')





@app.route("/new_user")
def new_user():
  return render_template("new_user.html")


@app.route("/new_user",  methods=['GET', 'POST'])
def return_information():
  error = None
  username = request.form['username']
  password = request.form['password']
  repassword = request.form['repassword']
  
  
  # check to see if the password creds are long enought ~7 length and contain a number
  if(len(password) < 7):
    flash('Password Must be Longer then 7 characters.')
    return redirect(url_for('new_user'))
  num_list = ['0','1','2','3','4','5','6','7','8','9','!','?']
  num_value = False
  for i in num_list:
    if i in password:
      num_value = True
    else:
      pass
  if(num_value == False):
    flash('Password must contain a number')
    return redirect(url_for('new_user'))

  # checks to see if the two passwords are correct. If they are not it reloads new_user. 
  new_user = UserLogin(username , password) 
  if(repassword != password):
    flash('Invalid password provided')
    return redirect(url_for('new_user'))
  else:
    # checks to see if the username is taken 
    new_user_status = new_user.check_user_exists(username)
    if(new_user_status == True):
      # if the username is taken then redirect back to the main page. 
      error = 'Username is taken'
      flash('Username is taken')
      return(redirect(url_for('new_user')))
    else:
      # if the username is not taken then create the new user into the database. 
      new_user.add_user()

  return('nothing')







if __name__ == "__main__":

  app.run(debug=True)

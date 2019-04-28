import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime

#app core 
app = Flask(__name__, instance_relative_config=True)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/practicedb'
SQLALCHEMY_TRACK_MODIFICATIONS = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    post_text = db.Column(db.String(255))

    def __init__(self, title, post_text):
        self.title = title
        self.post_text = post_text

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lesley.yc@gmail.com'
app.config['MAIL_PASSWORD'] = 'Retire69!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


@app.route("/")
def more():
	return render_template("home.html", title = "hello")

@app.route("/weekone")
def thebeginning():
	return render_template("thebeginning.html", title = "Week One")

@app.route("/weektwo")
def weektwo():
	return render_template("weektwo.html", title = "Week Two")

@app.route("/weekthree")
def weekthree():
	return render_template("weekthree.html", title = "Week Three")

@app.route("/weekfour")
def weekfour():
	return render_template("weekfour.html", title = "Week Four")

@app.route("/reflections")
def reflections():
	return render_template("reflections.html", title = "Reflections")

@app.route("/goals")
def goals():
	return render_template("goals.html", title = "Goals")

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html", title = "404"), 404

@app.route("/practiceForm", methods=["POST", "GET"])
def practiceForm():
    if request.method == "POST":
        username = request.form['username']        
        age = request.form['age']        
        email = request.form['email']        
        hobbies = request.form['hobbies']        
        return redirect(url_for("practiceData",                              
                                username=username,
                                age=age,
                                email=email,   
                                hobbies=hobbies))  
    return render_template("practiceForm.html", title = "Practice Form")

@app.route("/practiceData", methods=["GET"])
def practiceData():
    username = request.args.get('username')    
    age = request.args.get('age')    
    email = request.args.get('email')    
    hobbies = request.args.get('hobbies')    
    return render_template("practiceData.html",
                           username=username,                         
                           age=age,                          
                           email=email,                         
                           hobbies=hobbies
    )



@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate() == False: 
			flash('You must enter something into all of the fields')
			return render_template('contact.html', form = form)
		else:
			msg = Message('Hello', sender = 'lesley.yc@gmail.com', recipients = ['lesleyc@bu.edu'])
			msg.body = """
			From: %s %s <%s>
			%s
			""" % (form.firstName.data, form.lastName.data, form.email.data, form.message.data)
			mail.send(msg)
			return render_template('contact.html', success=True)
	elif request.method == 'GET':
		return render_template('contact.html',
			title = 'Contact Us',
			form = form)
	





#run server 
if __name__ == '__main__':
   app.run(debug = True)




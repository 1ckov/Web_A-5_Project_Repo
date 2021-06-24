from datetime import datetime
from re import S
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
from database import User
from passlib.hash import sha256_crypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)
from sqlalchemy_utils import EmailType

## User Table for storing Username, Password, Email and Language Preference
class User(db.Model):

    __tablename__ = "benutzer"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username= db.Column(db.String, unique=True, nullable=None)
    password = db.Column(db.String, unique=True, nullable=None)
    email = db.Column(EmailType, unique=True, nullable = None)
    language = db.Column(db.String)
    def __repr__(self):
        return "User: "+ str(self.username) + " /Id: "+ str(self.id) +" /Pass: "+ str(self.password)+ " /Email: " + str(self.email) + " /Language: " + str(self.language)

class Data(db.Model):
    id = db.Column(db.Integer,autoincrement=None,primary_key=True)
    gender = db.Column(db.String,nullable=True)
    first_name = db.Column(db.String,nullable=True)
    last_name = db.Column(db.String,nullable=True)
    date_of_birth = db.Column(db.Date,nullable=True)
## Changing Language
def changeLang(lang):
    session["lang"] = lang

def usernameExistsMessage():
    language_glob = session.get("lang")
    def bg():
        return "Потребителското име вече съществува! Моля, изберете друг." 
    def en():
        return "Username already exists! Please, choose another one."
    def de():
        return "Benutzername ist vergeben! Bitte wählen Sie einen anderen."
    def fr():
        return "Ce nom d'utilisateur existe déjà! S'il vous plaît, choisissez-en un autre."
    def default():
        return "You should not be seeing me"
    dict = {
        "bg": bg,
        "en" : en,
        "de" : de,
        "fr" : fr
    }
    return dict.get(language_glob,default)()

def emailExistsMessage():
    language_glob = session.get("lang")
    def bg():
        return "Имейлът вече се използва! Моля, изберете друг." 
    def en():
        return "Email is already in use! Please choose another one."
    def de():
        return "Email wird schon benutzt! Bitte wählen Sie eine andere!"
    def fr():
        return "Cet email est déjà utilisé! Veuillez en choisir un autre."
    def default():
        return "You should not be seeing me"
    dict = {
        "bg": bg,
        "en" : en,
        "de" : de,
        "fr" : fr
    }
    return dict.get(language_glob,default)()

def passwordRejectedMessage():
    language_glob = session.get("lang")
    def bg():
        return "Грешна парола или потребител!" 
    def en():
        return "Wrong password or user"
    def de():
        return "Falsches Passwort oder Nutzername"
    def fr():
        return "Mot de passe ou utilisateur erroné "
    def default():
        return "You should not be seeing me"
    dict = {
        "bg": bg,
        "en" : en,
        "de" : de,
        "fr" : fr
    }
    return dict.get(language_glob,default)()



# "Chose language" and "Loggin" page
@app.route('/', methods=['GET','POST'])
def index():
    if not (session.get("lang")) :                 
        session["lang"] = "en" 

    language_glob = session.get("lang")

    if not (session.get('logged_in') == True):
        if request.method == 'POST':
            if (request.form["username"] != None) and (request.form["password"] != None):

                usernamePOST=request.form["username"]
                passwordPOST=request.form["password"]
                passwordPOST =  sha256_crypt.encrypt("password")
                print(passwordPOST)


                user=User.query.filter_by(username = usernamePOST).first()
                
                #Loggin Procedure
                if user == None :
                    flash(passwordRejectedMessage())
                    return redirect('/')   

                elif(passwordPOST == str(user.password)):
                    session['logged_in'] = True
                    session['userId'] = user.id
                    changeLang(user.language)
                    return redirect('/' + user.language + '/home')
                
            flash(passwordRejectedMessage())
            return redirect('/')
        else: 

            if request.args.get('lang') != None:
                changeLang(request.args.get('lang'))
                return redirect('/')

            return render_template(language_glob + '/welcome.html', language = language_glob)
    else:

        return redirect("/"+ language_glob + "/home")

# Registration Page 
@app.route('/<string:lang>/register', methods=['GET','POST'])
def registration(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        
        username = request.form['userNameReg']
        password= request.form['password']
        password = sha256_crypt.encrypt('password')
        email = request.form['email']
        language= request.form['language']

        if User.query.filter_by(username = username).first() :
            flash(usernameExistsMessage())
            return redirect('/'+ language_glob+'/register')

        if User.query.filter_by(email = email).first() :
            flash(emailExistsMessage())
            return redirect('/'+ language_glob+'/register')

        ########## Put data from forms into DB ##########
        new_user= User(username = username, password= password, email= email, language= language)
        db.session.add(new_user) 
        db.session.commit()  
        #################################################
        
        if request.form['language'] != None:
            changeLang(request.form['language'])
            language_glob = request.form['language']
        session["logged_in"] = True
        session['userId'] = new_user.id
        return redirect('/' + language_glob + '/home')

    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/register')
        return render_template( language_glob + '/register.html', language = language_glob)

# Logout Function 
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect("/")

# Landing Page for each language
@app.route('/<string:lang>/home')
def home(lang):
    language_glob = session.get("lang")
     
    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + language_glob + '/home')
    return render_template(language_glob + '/home.html', language = language_glob)

# GEZ Explanation
@app.route('/<string:lang>/gez/gez_explanation', methods=['GET','POST'])
def gez_explanation(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        return redirect('/' + language_glob + '/gez/general_information1')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/gez_explanation')
        return render_template(language_glob + '/gez_explanation.html', language = language_glob)

########################################################################################
###################################### General Information #############################
########################################################################################

# The General information Form Part 1
@app.route('/<string:lang>/gez/general_information1', methods=['GET','POST'])
def general_information1(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/general_information2' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/general_information1')
        return render_template(language_glob + '/general_information/general_information1.html', language = language_glob)

# The General information Form Part 2
@app.route('/<string:lang>/gez/general_information2', methods=['GET','POST'])
def general_information2(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/general_information3' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/general_information2')
        return render_template(language_glob + '/general_information/general_information2.html', language = language_glob)

# The General information Form Part 3
@app.route('/<string:lang>/gez/general_information3', methods=['GET','POST'])
def general_information3(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress1' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/general_information3')
        return render_template(language_glob + '/general_information/general_information3.html', language = language_glob)

########################################################################################
###################################### Adress ##########################################
########################################################################################

# The Adress Form Part 1 
@app.route('/<string:lang>/gez/adress1', methods=['GET','POST'])
def adress1(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress2' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/adress1')
        return render_template(language_glob + '/adress/adress1.html', language = language_glob)

# The Adress Form Part 2 
@app.route('/<string:lang>/gez/adress2', methods=['GET','POST'])
def adress2(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress3' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/adress2')
        return render_template(language_glob + '/adress/adress2.html', language = language_glob)

# The Adress Form Part 3 
@app.route('/<string:lang>/gez/adress3', methods=['GET','POST'])
def adress3(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress4' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/adress3')
        return render_template(language_glob + '/adress/adress3.html', language = language_glob)

# The Adress Form Part 4 
@app.route('/<string:lang>/gez/adress4', methods=['GET','POST'])
def adress4(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress5' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/adress4')
        return render_template(language_glob + '/adress/adress4.html', language = language_glob)

# The Adress Form Part 5 
@app.route('/<string:lang>/gez/adress5', methods=['GET','POST'])
def adress5(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods1' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/adress5')
        return render_template(language_glob + '/adress/adress5.html', language = language_glob)

########################################################################################
############################### Payment Methods ########################################
########################################################################################

# The Payment Methods Form Part 1
@app.route('/<string:lang>/gez/payment_methods1', methods=['GET','POST']) 
def payment_methods1(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        
        #################################################
            return redirect('/' + language_glob + '/gez/payment_methods2')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/payment_methods1')
        return render_template(language_glob + '/payment_methods/payment_methods1.html', language = language_glob)


# The Payment Methods Form Part 2
@app.route('/<string:lang>/gez/payment_methods2', methods=['GET','POST']) 
def payment_methods2(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        
        #################################################
        if request.form["type"] == "sepa":
            return redirect('/' + language_glob + '/gez/sepa1' )
        elif request.form["type"] == "bank":
            return redirect('/' + language_glob + '/gez/final')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/payment_methods2')
        return render_template(language_glob + '/payment_methods/payment_methods2.html', language = language_glob)

########################################################################################
###################################### Sepa ############################################
########################################################################################

# The Sepa Form Part 1
@app.route('/<string:lang>/gez/sepa1', methods=['GET','POST'])
def sepa1(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa2' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/sepa1')
        return render_template(language_glob + '/sepa/sepa1.html', language = language_glob)


# The Sepa Form Part 2
@app.route('/<string:lang>/gez/sepa2', methods=['GET','POST'])
def sepa2(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa3' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/sepa2')
        return render_template(language_glob + '/sepa/sepa2.html', language = language_glob)


# The Sepa Form Part 3
@app.route('/<string:lang>/gez/sepa3', methods=['GET','POST'])
def sepa3(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa4' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/sepa3')
        return render_template(language_glob + '/sepa/sepa3.html', language = language_glob)


# The Sepa Form Part 4
@app.route('/<string:lang>/gez/sepa4', methods=['GET','POST'])
def sepa4(lang):
    language_glob = session.get("lang")
     
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/final' )
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect ('/' + request.args.get('lang') + '/gez/sepa4')
        return render_template(language_glob + '/sepa/sepa4.html', language = language_glob)

# Final notice page for GEZ
@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    language_glob = session.get("lang")
     
    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect ('/' + request.args.get('lang') + '/gez/final')
    return render_template(language_glob + '/final.html', language = language_glob)
    

# About us page
@app.route('/<string:lang>/about_us')
def about(lang):
    language_glob = session.get("lang")
     
    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect ('/' + request.args.get('lang') + '/about_us')
    return render_template(language_glob + '/about_us.html', language = language_glob)

@app.route('/<string:lang>/privacy_policy')
def privacy_policy(lang):
    language_glob = session.get("lang")
     
    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect ('/' + request.args.get('lang') + '/privacy_policy')
    return render_template(language_glob + '/privacy_policy.html', language = language_glob)


@app.route('/<string:lang>/legal_notice')
def legal_notice(lang):
    language_glob = session.get("lang")
     
    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect ('/' + request.args.get('lang') + '/legal_notice')
    return render_template(language_glob + '/legalNotice.html', language = language_glob)



if __name__ == "__main__":
    app.secret_key = str(os.urandom(12))
    app.run(debug=True)
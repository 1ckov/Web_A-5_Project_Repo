from datetime import datetime
from re import I, S
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
from database import User, Data
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import EmailType
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
#db_session = SQLAlchemy(app)
session_variables = {"gender": "", "first_name": "", "last_name":  "", "date_of_birth": "", "registration_date": "", "street": "", "streetnumber": "", "address_addition": "", "zip_code": "", "city": "",
                     "phone_number": "", "timespan": "", "type_of_transfer": "", "name_sepa": "", "street_sepa": "", "streetnumber_sepa": "", "zip_code_sepa": "", "city_sepa": "", "IBAN": "", "BIC": "", "credit_institution": ""}
session_names = ["gender", "first_name", "last_name", "date_of_birth",
                 "registration_date", "street", "streetnumber", "address_addition",
                 "zip_code", "city", "phone_number", "timespan", "type_of_transfer",
                 "name_sepa", "street_sepa", "streetnumber_sepa", "zip_code_sepa",
                 "city_sepa", "IBAN", "BIC", "credit_institution"]
POST_names = ["gender", "firstName", "lastName", "dateOfBirth", "date_reg", "street", "street_nr", "adress_additions", "zip_code",
              "city", "phone_number", "timespan", "type", "fullName", "street", "street_nr", "ZIP_code", "area", "IBAN", "BIC", "credit_institution"]

engine = create_engine('sqlite:///app.db', echo=True)


# Changing Language
def changeLang(lang):
    session["lang"] = lang


def addToDict(name, value, array):
    print(name)
    print(value)
    print(array)
    if(value != ""):
        array[name] = value
        return array
    return array


def getSessionName(stepNumber):
    global session_names
    return session_names[stepNumber]


def getPOSTName(stepNumber):
    global POST_names
    return POST_names[stepNumber]


def addToSV(name, value):
    temp = session["session_variables"]
    temp[name] = value
    session["session_variables"] = temp
    if session.get("logged_in"):
        Session = sessionmaker(bind=engine)
        db_session = Session()
        print(db_session.query(Data).filter_by(
            user_id=session["uid"]).update({name: value}))
        db_session.commit()


def populateSV(uid):
    global session_variables
    temp = session_variables.copy()
    print(temp)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    db_data = db_session.query(Data).filter_by(user_id=session["uid"]).first()
    temp = addToDict("gender", db_data.gender, temp)
    temp = addToDict("first_name", db_data.first_name, temp)
    temp = addToDict("last_name", db_data.last_name, temp)
    temp = addToDict("date_of_birth", db_data.date_of_birth, temp)
    temp = addToDict("registration_date", db_data.registration_date, temp)
    temp = addToDict("street", db_data.street, temp)
    temp = addToDict("streetnumber", db_data.streetnumber, temp)
    temp = addToDict("address_addition", db_data.address_addition, temp)
    temp = addToDict("zip_code", db_data.zip_code, temp)
    temp = addToDict("city", db_data.city, temp)
    temp = addToDict("phone_number", db_data.phone_number, temp)
    temp = addToDict("timespan", db_data.timespan, temp)
    temp = addToDict("type_of_transfer", db_data.type_of_transfer, temp)
    temp = addToDict("name_sepa", db_data.name_sepa, temp)
    temp = addToDict("street_sepa", db_data.street_sepa, temp)
    temp = addToDict("streetnumber_sepa", db_data.streetnumber_sepa, temp)
    temp = addToDict("zip_code_sepa", db_data.zip_code_sepa, temp)
    temp = addToDict("city_sepa", db_data.city_sepa, temp)
    temp = addToDict("IBAN", db_data.IBAN, temp)
    temp = addToDict("BIC", db_data.BIC, temp)
    temp = addToDict("credit_institution", db_data.credit_institution, temp)
    session["session_variables"] = temp


def hashPwd(pwd):
    salt = (b"100000")
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        pwd.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    )
    return key


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
        "en": en,
        "de": de,
        "fr": fr
    }
    return dict.get(language_glob, default)()


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
        "en": en,
        "de": de,
        "fr": fr
    }
    return dict.get(language_glob, default)()


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
        "en": en,
        "de": de,
        "fr": fr
    }
    return dict.get(language_glob, default)()


# "Chose language" and "Loggin" page
@app.route('/', methods=['GET', 'POST'])
def index():
    global session_variables

    # Setting default Language
    if not (session.get("lang")):
        session["lang"] = "en"

    # Saving language for further use
    language_glob = session.get("lang")

    # If User not logged in
    if not (session.get('logged_in') == True):

        # If User is signing in
        if request.method == 'POST':

            # Check if Passwords and Username are set.
            if (request.form["username"] != "") and (request.form["password"] != ""):

                # Extract Password
                usernamePOST = request.form["username"]

                # And Username
                passwordPOST = str(hashPwd(request.form["password"]))

                # Open communication to DB
                Session = sessionmaker(bind=engine)
                db_session = Session()

                # Check if user Exists
                user = db_session.query(User).filter_by(
                    username=usernamePOST).first()

                # Password or Username rejected
                if user == None:
                    flash(passwordRejectedMessage())
                    return redirect('/')

                # If passwords match
                elif(passwordPOST == user.password):
                    # User gets logged in and his user id gets saved
                    session['logged_in'] = True
                    session['uid'] = int(user.id)
                    populateSV(user.id)

# Check if there is data from DB

                    # Create a session variables dict for PDF Creation
                    changeLang(user.language)
                    return redirect('/' + user.language + '/home')

            flash(passwordRejectedMessage())
            return redirect('/')
        else:

            if request.args.get('lang') != None:
                changeLang(request.args.get('lang'))
                return redirect('/')

            return render_template(language_glob + '/welcome.html', language=language_glob)
    else:

        return redirect("/" + language_glob + "/home")

# Registration Page


@app.route('/<string:lang>/register', methods=['GET', 'POST'])
def registration(lang):
    language_glob = session.get("lang")
    global session_variables
    session["session_variables"] = session_variables.copy()
    if request.method == 'POST':

        # Getting Post Data
        username = request.form['userNameReg']
        password = str(hashPwd(request.form['password']))
        email = request.form['email']
        language = request.form['language']

        # Opening a Session with the DB server
        Session = sessionmaker(bind=engine)
        db_session = Session()

        if db_session.query(User).filter_by(username=username).first():
            flash(usernameExistsMessage())
            return redirect('/' + language_glob+'/register')

        if db_session.query(User).filter_by(email=email).first():
            flash(emailExistsMessage())
            return redirect('/' + language_glob+'/register')

        ########## Put data from forms into DB ##########
        # New User
        new_user = User(username=username, password=password,
                        email=email, language=language)
        db_session.add(new_user)
        db_session.commit()
        user_id = db_session.query(User).filter_by(
            username=username).first().id
        gender = request.form.get("gender")
        addToSV("gender", gender)
        first_name = request.form.get("firstName")
        addToSV("first_name", first_name)
        last_name = request.form.get("lastName")
        addToSV("last_name", last_name)

# Check if date of birth is future
        
        date_of_birth = request.form.get("dateOfBirth")
        addToSV("date_of_birth", date_of_birth)
        new_data = Data(user_id=user_id,
                        gender=gender,
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        registration_date="",
                        street="",
                        streetnumber="",
                        address_addition="",
                        zip_code="",
                        city="",
                        phone_number="",
                        timespan="",
                        type_of_transfer="",
                        name_sepa="",
                        street_sepa="",
                        streetnumber_sepa="",
                        zip_code_sepa="",
                        city_sepa="",
                        IBAN="",
                        BIC="",
                        credit_institution=""
                        )
        db_session.add(new_data)
        db_session.commit()
        #################################################

        if request.form['language'] != None:
            changeLang(request.form['language'])
            language_glob = request.form['language']

        session["logged_in"] = True
        session['uid'] = user_id
        return redirect('/' + language_glob + '/home')

    else:

        if request.args.get('lang') != None:

            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/register')

        return render_template(language_glob + '/register.html', language=language_glob)

# Logout Function


@app.route('/logout')
def logout():
    global session_variables
    session['logged_in'] = False
    session["session_variables"] = session_variables
    return redirect("/")

# Landing Page for each language


@app.route('/<string:lang>/home')
def home(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + language_glob + '/home')
    return render_template(language_glob + '/home.html', language=language_glob)

# GEZ Explanation


@app.route('/<string:lang>/gez/gez_explanation', methods=['GET', 'POST'])
def gez_explanation(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        return redirect('/' + language_glob + '/gez/general_information1')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/gez_explanation')
        return render_template(language_glob + '/gez_explanation.html', language=language_glob)

########################################################################################
###################################### General Information #############################
########################################################################################

# The General information Form Part 1


@app.route('/<string:lang>/gez/general_information1', methods=['GET', 'POST'])
def general_information1(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Gender
        POSTname = getPOSTName(0)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(0)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/general_information2')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/general_information1')
        fields = session.get("session_variables")
        return render_template(language_glob + '/general_information/general_information1.html', language=language_glob, fields=session.get("session_variables"))

# The General information Form Part 2


@app.route('/<string:lang>/gez/general_information2', methods=['GET', 'POST'])
def general_information2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Last Name
        POSTname = getPOSTName(1)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(1)
        addToSV(POSTname, genderPOST)
        # First Name
        POSTname = getPOSTName(2)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(2)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/general_information3')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/general_information2')
        return render_template(language_glob + '/general_information/general_information2.html', language=language_glob, fields=session.get("session_variables"))

# The General information Form Part 3


@app.route('/<string:lang>/gez/general_information3', methods=['GET', 'POST'])
def general_information3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Date of birth
        POSTname = getPOSTName(3)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(3)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress1')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/general_information3')
        return render_template(language_glob + '/general_information/general_information3.html', language=language_glob, fields=session.get("session_variables"))

########################################################################################
###################################### Adress ##########################################
########################################################################################

# The Adress Form Part 1


@app.route('/<string:lang>/gez/adress1', methods=['GET', 'POST'])
def adress1(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Date of registration
        POSTname = getPOSTName(4)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(4)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress2')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress1')
        return render_template(language_glob + '/adress/adress1.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 2


@app.route('/<string:lang>/gez/adress2', methods=['GET', 'POST'])
def adress2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Street
        POSTname = getPOSTName(5)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(5)
        addToSV(POSTname, genderPOST)
        # Street Nr.
        POSTname = getPOSTName(6)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(6)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress3')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress2')
        return render_template(language_glob + '/adress/adress2.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 3


@app.route('/<string:lang>/gez/adress3', methods=['GET', 'POST'])
def adress3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Adress additional.
        POSTname = getPOSTName(7)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(7)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress4')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress3')
        return render_template(language_glob + '/adress/adress3.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 4


@app.route('/<string:lang>/gez/adress4', methods=['GET', 'POST'])
def adress4(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # ZIP
        POSTname = getPOSTName(8)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(8)
        addToSV(POSTname, genderPOST)
        # City
        POSTname = getPOSTName(9)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(9)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress5')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress4')
        return render_template(language_glob + '/adress/adress4.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 5


@app.route('/<string:lang>/gez/adress5', methods=['GET', 'POST'])
def adress5(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Phone Nr.
        POSTname = getPOSTName(10)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(10)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods1')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress5')
        return render_template(language_glob + '/adress/adress5.html', language=language_glob, fields=session.get("session_variables"))

########################################################################################
############################### Payment Methods ########################################
########################################################################################

# The Payment Methods Form Part 1


@app.route('/<string:lang>/gez/payment_methods1', methods=['GET', 'POST'])
def payment_methods1(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Timespan.
        POSTname = getPOSTName(11)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(11)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods2')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/payment_methods1')
        return render_template(language_glob + '/payment_methods/payment_methods1.html', language=language_glob, fields=session.get("session_variables"))


# The Payment Methods Form Part 2
@app.route('/<string:lang>/gez/payment_methods2', methods=['GET', 'POST'])
def payment_methods2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Type of Transfer.
        POSTname = getPOSTName(12)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(12)
        addToSV(POSTname, genderPOST)
        #################################################
        if request.form["type"] == "sepa":
            return redirect('/' + language_glob + '/gez/sepa1')
        elif request.form["type"] == "bank":
            return redirect('/' + language_glob + '/gez/final')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/payment_methods2')
        return render_template(language_glob + '/payment_methods/payment_methods2.html', language=language_glob, fields=session.get("session_variables"))

########################################################################################
###################################### Sepa ############################################
########################################################################################

# The Sepa Form Part 1


@app.route('/<string:lang>/gez/sepa1', methods=['GET', 'POST'])
def sepa1(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Fullname.
        POSTname = getPOSTName(13)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(13)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa2')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa1')
        return render_template(language_glob + '/sepa/sepa1.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 2
@app.route('/<string:lang>/gez/sepa2', methods=['GET', 'POST'])
def sepa2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Street.
        POSTname = getPOSTName(14)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(14)
        addToSV(POSTname, genderPOST)
        # Street Nr.
        POSTname = getPOSTName(15)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(15)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa3')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa2')
        return render_template(language_glob + '/sepa/sepa2.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 3
@app.route('/<string:lang>/gez/sepa3', methods=['GET', 'POST'])
def sepa3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # ZIP.
        POSTname = getPOSTName(16)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(16)
        addToSV(POSTname, genderPOST)
        # City.
        POSTname = getPOSTName(17)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(17)
        addToSV(POSTname, genderPOST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa4')
    else:
        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa3')
        return render_template(language_glob + '/sepa/sepa3.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 4
@app.route('/<string:lang>/gez/sepa4', methods=['GET', 'POST'])
def sepa4(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # IBAN.
        POSTname = getPOSTName(18)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(18)
        addToSV(POSTname, genderPOST)
        # BIC.
        POSTname = getPOSTName(19)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(19)
        addToSV(POSTname, genderPOST)
        # Credit Institution.
        POSTname = getPOSTName(20)
        genderPOST = request.form[POSTname]
        POSTname = getSessionName(20)
        addToSV(POSTname, genderPOST)

        sv = session.get("session_varaibles")
     

        #################################################
        return redirect('/' + language_glob + '/gez/final')

    else:

        if request.args.get('lang') != None:
            changeLang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa4')
        return render_template(language_glob + '/sepa/sepa4.html', language=language_glob, fields=session.get("session_variables"))

# Final notice page for GEZ


@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/gez/final')
    return render_template(language_glob + '/final.html', language=language_glob)


# About us page
@app.route('/<string:lang>/about_us')
def about(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/about_us')
    return render_template(language_glob + '/about_us.html', language=language_glob)


@app.route('/<string:lang>/privacy_policy')
def privacy_policy(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/privacy_policy')
    return render_template(language_glob + '/privacy_policy.html', language=language_glob)


@app.route('/<string:lang>/legal_notice')
def legal_notice(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        changeLang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/legal_notice')
    return render_template(language_glob + '/legalNotice.html', language=language_glob)


if __name__ == "__main__":
    app.secret_key = str(os.urandom(12))
    app.run(debug=True)

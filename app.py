# -*- coding: utf-8> -*-

from flask import Flask, flash, redirect, render_template, request, session
import os
from database import User, Data
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pypdftk
import datetime
from os.path import exists


app = Flask(__name__)

session_variables = {"gender": "", "first_name": "", "last_name":  "", "date_of_birth": "", "registration_date": "", "street": "", "streetnumber": "", "address_addition": "", "zip_code": "", "city": "",
                     "phone_number": "", "timespan": "", "type_of_transfer": "", "name_sepa": "", "street_sepa": "", "streetnumber_sepa": "", "zip_code_sepa": "", "city_sepa": "", "IBAN": "", "BIC": "", "credit_institution": ""}
session_names = ["gender", "first_name", "last_name", "date_of_birth",
                 "registration_date", "street", "streetnumber", "address_addition",
                 "zip_code", "city", "phone_number", "timespan", "type_of_transfer",
                 "name_sepa", "street_sepa", "streetnumber_sepa", "zip_code_sepa",
                 "city_sepa", "IBAN", "BIC", "credit_institution"]
POST_names = ["gender", "firstName", "lastName", "dateOfBirth", "date_reg", "street", "street_nr", "adress_additions", "zip_code",
              "city", "phone_number", "timespan", "type", "fullName", "street", "street_nr", "ZIP_code", "area", "IBAN", "BIC", "credit_institution"]

xml_variables = {
    "Anrede": ["Frau", "Herr"],
    "Vorname": "",  # Max length 28
    "TitelNachname": "",  # Max length 19
    "Geburtsdatum": "",  # Max length 8
    "Anmeldedatum": "",  # Max length 6, only month and year
    "Adresszusatz": "",  # Max length 22
    "Stra&#223;e" : "", # Max length 22 
    "Hausnummer": "",  # Max length 5
    "PLZ": "",  # Max length 5
    "Ort": "",  # Max length 22
    "Zahlungsrhythmus": ["in der Mitte eines Dreimonatszeitraums",
                        "viertelj&#228;hrlich im Voraus",
                        "halbj&#228;hrlich im Voraus", "j&#228;hrlich im Voraus"],
    "Zahlungsweise": ["Lastschrift", "&#220;berweisung"],
    "Stra&#223;e_Lastschrift": "",  # Max length 22
    "IBAN": "",  # Max length 28
    "BIC": "",  # Max length 11
    "Kreditinstitut": "",  # Max length 16
    "NameLastschrift": "",  # Max length 28
    "HausnummerLastschrift": "",  # Max length 5
    "OrtLastschrift": "",  # Max length 22
    "PLZLastschrift": "",  # Max length 5
    "Telefonnummer": "",  # Max length 17
}

engine = create_engine('sqlite:///app.db', echo=True)


# Changing Language
def change_lang(lang):
    session["lang"] = lang

# Check if date given is in the future

def check_future_date(date_str):
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    date_given = datetime.datetime(year,month,day)
    now = datetime.datetime.now()
    if (date_given > now):
        return True
    else: 
        return False

# Filling our a pdf with a dictionary

def fill_pdf(data):
    global xml_variables
    xml_var = xml_variables.copy()

    # Gender     
    if(data.get("gender") == "Male"):
        xml_var["Anrede"] = xml_var["Anrede"][1]
    elif(data.get("gender") == "Female"):
        xml_var["Anrede"] = xml_var["Anrede"][0]


    # First Name 
    fname_str = data.get("first_name")
    if (len(fname_str) > 28 ):
        fname_str= fname_str[0 : 29]
    xml_var["Vorname"] = fname_str

    # Last Name
    lname_str = data.get("last_name")
    if (len(lname_str) > 19 ):
        lname_str = lname_str[0 : 20]
    xml_var["TitelNachname"] = lname_str
    
    # Birthdate 
    date_str = data.get("date_of_birth")           
    if (len(date_str)  > 8 ): 
        year = date_str[0:4]
        month = date_str[5:7]
        day = date_str[8:10]
        date_str = day + month + year
    else:
        date_str = ""
    xml_var["Geburtsdatum"] = date_str

    # Date of registration
    reg_str = data.get("registration_date")         
    if (len(reg_str) > 6 ):
        year = reg_str[0:4]
        month = reg_str[5:7]
        reg_str = month + year
    else:
        reg_str = ""
    xml_var["Anmeldedatum"] = reg_str
    
    # Address addition
    adr_addition = data.get("address_addition")
    if (len(fname_str) > 22 ):
        adr_addition = adr_addition[0 : 23]
    xml_var["Adresszusatz"] = adr_addition

    # Street Name
    street_name = data.get("street")
    if (len(street_name) > 22 ):
        street_name = street_name[0 : 23]
    xml_var["Stra&#223;e"] = street_name

    # Street Number
    street_num = data.get("streetnumber")
    if (len(street_num) > 5 ):
        street_num = street_num[0 : 6]
    xml_var["Hausnummer"] = street_num
    
    # ZIP Code
    zip_code = str(data.get("zip_code"))
    if (len(zip_code) > 5 ):
        zip_code = zip_code[0 : 6]
    xml_var["PLZ"] = zip_code

    # City 
    city_name = data.get("city")
    if (len(city_name) > 22 ):
        city_name = city_name[0 : 23]
    xml_var["Ort"] = city_name

    # Payment Cycle
    pay_cicle = int(data.get("timespan"))
    if(pay_cicle == 1):
        xml_var["Zahlungsrhythmus"] = xml_var["Zahlungsrhythmus"][0]
    elif(pay_cicle == 2):
        xml_var["Zahlungsrhythmus"] = xml_var["Zahlungsrhythmus"][1]
    elif(pay_cicle == 3):
        xml_var["Zahlungsrhythmus"] = xml_var["Zahlungsrhythmus"][2]
    elif(pay_cicle == 4):
        xml_var["Zahlungsrhythmus"] = xml_var["Zahlungsrhythmus"][3]
    
    # Type of Payment
    pay_type = data.get("type_of_transfer")
    if(pay_type == "sepa"):
        xml_var["Zahlungsweise"] = xml_var["Zahlungsweise"][0]
    elif(pay_type == "bank"):
        xml_var["Zahlungsweise"] = xml_var["Zahlungsweise"][1]

    # Street Sepa 
    street_sepa = data.get("street_sepa") 
    if (len(street_sepa) > 22 ):
        street_sepa = street_sepa[0 : 23]
    xml_var["Stra&#223;e_Lastschrift"] = street_sepa
    
    # IBAN
    iban_sepa = data.get("IBAN") 
    if (len(iban_sepa) > 28 ):
        iban_sepa = iban_sepa[0 : 29]
    xml_var["IBAN"] = iban_sepa
    
    # BIC
    bic_sepa = data.get("BIC") 
    if (len(bic_sepa) > 11 ):
        bic_sepa = bic_sepa[0 : 12]
    xml_var["BIC"] = bic_sepa

    # Bank
    bank_sepa = data.get("credit_institution") 
    if (len(bank_sepa) > 16 ):
        bank_sepa = bank_sepa[0 : 17]
    xml_var["Kreditinstitut"] = bank_sepa

    # Name of payment beneficiery 
    name_sepa = data.get("name_sepa") 
    if (len(name_sepa) > 28 ):
        name_sepa = name_sepa [0 : 29]
    xml_var["NameLastschrift"] = name_sepa
    
    # Street number of payment beneficiery 
    streetnumber_sepa = data.get("streetnumber_sepa") 
    if (len(streetnumber_sepa) > 5 ):
        streetnumber_sepa = streetnumber_sepa [0 : 6]
    xml_var["HausnummerLastschrift"] = streetnumber_sepa

    # City of payment beneficiery
    city_sepa = data.get("city_sepa") 
    if (len(city_sepa) > 22 ):
        city_sepa = street_sepa [0 : 23]
    xml_var["OrtLastschrift"] = city_sepa

    # ZIP number of payment beneficiery
    zip_sepa = data.get("zip_code_sepa") 
    if (len(zip_sepa) > 5 ):
        zip_sepa = zip_sepa [0 : 6]
    xml_var["PLZLastschrift"] = zip_sepa

    # Personal Telephone number
    phone_number = data.get("phone_number") 
    if (len(phone_number) > 17 ):
        phone_number = phone_number [0 : 18]
    xml_var["Telefonnummer"] = phone_number

    # Generating PDF    
    if exists("gez.pdf"):
        if not exists("pdf_storage/" + str(session["uid"])):
            os.mkdir("pdf_storage/" + str(session["uid"]))
    pdf_name = 'pdf_storage/' + str(session["uid"]) + "/GEZ_Form_" + str(datetime.datetime.now())[0:10] + ".pdf"
    pypdftk.fill_form('gez.pdf', xml_var ,pdf_name )



# Helper Method for fiiling arrays


def add_to_dict(name, value, array):
    if(value != ""):
        array[name] = value
        return array
    return array

# Returns a "Session Variable" name based on the numerical postion of the field


def get_session_name(stepNumber):
    global session_names
    return session_names[stepNumber]

# Return a "HTML field" name based on its numerical position.


def get_POST_name(stepNumber):
    global POST_names
    return POST_names[stepNumber]


# Puts a variable in the SV and if user is logged in, also in the DB


def fill_SV_and_DB(name, value):
    temp = session["session_variables"]
    temp[name] = value
    session["session_variables"] = temp
    if session.get("logged_in"):
        Session = sessionmaker(bind=engine)
        db_session = Session()
        print(db_session.query(Data).filter_by(
            user_id=session["uid"]).update({name: value}))
        db_session.commit()


# Fills SV array with data retrieved from the DB


def populate_SV(uid):
    global session_variables
    temp = session_variables.copy()
    Session = sessionmaker(bind=engine)
    db_session = Session()
    db_data = db_session.query(Data).filter_by(user_id=uid).first()
    temp = add_to_dict("gender", db_data.gender, temp)
    temp = add_to_dict("first_name", db_data.first_name, temp)
    temp = add_to_dict("last_name", db_data.last_name, temp)
    temp = add_to_dict("date_of_birth", db_data.date_of_birth, temp)
    temp = add_to_dict("registration_date", db_data.registration_date, temp)
    temp = add_to_dict("street", db_data.street, temp)
    temp = add_to_dict("streetnumber", db_data.streetnumber, temp)
    temp = add_to_dict("address_addition", db_data.address_addition, temp)
    temp = add_to_dict("zip_code", db_data.zip_code, temp)
    temp = add_to_dict("city", db_data.city, temp)
    temp = add_to_dict("phone_number", db_data.phone_number, temp)
    temp = add_to_dict("timespan", db_data.timespan, temp)
    temp = add_to_dict("type_of_transfer", db_data.type_of_transfer, temp)
    temp = add_to_dict("name_sepa", db_data.name_sepa, temp)
    temp = add_to_dict("street_sepa", db_data.street_sepa, temp)
    temp = add_to_dict("streetnumber_sepa", db_data.streetnumber_sepa, temp)
    temp = add_to_dict("zip_code_sepa", db_data.zip_code_sepa, temp)
    temp = add_to_dict("city_sepa", db_data.city_sepa, temp)
    temp = add_to_dict("IBAN", db_data.IBAN, temp)
    temp = add_to_dict("BIC", db_data.BIC, temp)
    temp = add_to_dict("credit_institution", db_data.credit_institution, temp)
    session["session_variables"] = temp

# Hashesh password with pdkf2_hmac algorithm, should be replaced cause fo DB issues


def hash_pwd(pwd):
    salt = (b"100000")
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        pwd.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    )
    return key

# Helper method to retrieve a Message based on the currently set language.


def uname_exists():
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

# Helper method to retrieve a Message based on the currently set language.


def email_exists():
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

# Helper method to retrieve a Message based on the currently set language.


def passwd_rejected():
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


def date_rejected():
    language_glob = session.get("lang")

    def bg():
        return "Дадената дата е в бъдещето!"

    def en():
        return "The date you have given is in the Future!"

    def de():
        return "Das Datum das Sie eingetragen haben ist in der Zukunft!"

    def fr():
        return "La date que vous avez donnée est dans le futur! "

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
    session["session_variables"] = session_variables.copy()
    # If User not logged in
    if not (session.get('logged_in') == True):

        # If User is signing in
        if request.method == 'POST':

            # Check if Passwords and Username are set.
            if (request.form["username"] != "") and (request.form["password"] != ""):

                # Extract Password
                usernamePOST = request.form["username"]

                # And Username
                passwordPOST = str(hash_pwd(request.form["password"]))

                # Open communication to DB
                Session = sessionmaker(bind=engine)
                db_session = Session()

                # Check if user Exists
                user = db_session.query(User).filter_by(
                    username=usernamePOST).first()

                # Password or Username rejected
                if user == None:
                    flash(passwd_rejected())
                    return redirect('/')

                # If passwords match
                elif(passwordPOST == user.password):
                    # User gets logged in and his user id gets saved
                    session['logged_in'] = True
                    session['uid'] = int(user.id)
                    populate_SV(user.id)

# Check if there is data from DB

                    # Create a session variables dict for PDF Creation
                    change_lang(user.language)
                    return redirect('/' + user.language + '/home')

            flash(passwd_rejected())
            return redirect('/')
        else:

            if request.args.get('lang') != None:
                change_lang(request.args.get('lang'))
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
        password = str(hash_pwd(request.form['password']))
        email = request.form['email']
        language = request.form['language']

        # Opening a Session with the DB server
        Session = sessionmaker(bind=engine)
        db_session = Session()

        if db_session.query(User).filter_by(username=username).first():
            flash(uname_exists())
            return redirect('/' + language_glob+'/register')

        if db_session.query(User).filter_by(email=email).first():
            flash(email_exists())
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
        fill_SV_and_DB("gender", gender)
        first_name = request.form.get("firstName")
        fill_SV_and_DB("first_name", first_name)
        last_name = request.form.get("lastName")
        fill_SV_and_DB("last_name", last_name)

# Check if date of birth is future

        date_of_birth = request.form.get("dateOfBirth")
        if (check_future_date(date_of_birth)):
            flash(date_rejected)
            return redirect('/' + language_glob +'/register')
        fill_SV_and_DB("date_of_birth", date_of_birth)

        # Filling in possible data and setting dummy values for missing values
        # New Data
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
            change_lang(request.form['language'])
            language_glob = request.form['language']

        session["logged_in"] = True
        session['uid'] = user_id
        return redirect('/' + language_glob + '/home')

    else:

        if request.args.get('lang') != None:

            change_lang(request.args.get('lang'))
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
    fill_pdf(session["session_variables"])
    if request.args.get('lang') != None:
        change_lang(request.args.get('lang'))
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
            change_lang(request.args.get('lang'))
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
        POSTname = get_POST_name(0)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(0)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/general_information2')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/general_information1')
        return render_template(language_glob + '/general_information/general_information1.html', language=language_glob, fields=session.get("session_variables"))

# The General information Form Part 2


@app.route('/<string:lang>/gez/general_information2', methods=['GET', 'POST'])
def general_information2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Last Name
        POSTname = get_POST_name(1)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(1)
        fill_SV_and_DB(POSTname, var_POST)
        # First Name
        POSTname = get_POST_name(2)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(2)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/general_information3')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/general_information2')
        return render_template(language_glob + '/general_information/general_information2.html', language=language_glob, fields=session.get("session_variables"))

# The General information Form Part 3


@app.route('/<string:lang>/gez/general_information3', methods=['GET', 'POST'])
def general_information3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Date of birth
        POSTname = get_POST_name(3)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(3)
        if (check_future_date(var_POST)):
            flash(date_rejected())
            return redirect('/' + language_glob + '/gez/general_information3')
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress1')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
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
        POSTname = get_POST_name(4)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(4)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress2')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress1')
        return render_template(language_glob + '/adress/adress1.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 2


@app.route('/<string:lang>/gez/adress2', methods=['GET', 'POST'])
def adress2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Street
        POSTname = get_POST_name(5)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(5)
        fill_SV_and_DB(POSTname, var_POST)
        # Street Nr.
        POSTname = get_POST_name(6)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(6)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress3')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress2')
        return render_template(language_glob + '/adress/adress2.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 3


@app.route('/<string:lang>/gez/adress3', methods=['GET', 'POST'])
def adress3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Adress additional.
        POSTname = get_POST_name(7)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(7)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress4')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress3')
        return render_template(language_glob + '/adress/adress3.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 4


@app.route('/<string:lang>/gez/adress4', methods=['GET', 'POST'])
def adress4(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # ZIP
        POSTname = get_POST_name(8)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(8)
        fill_SV_and_DB(POSTname, var_POST)
        # City
        POSTname = get_POST_name(9)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(9)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/adress5')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/adress4')
        return render_template(language_glob + '/adress/adress4.html', language=language_glob, fields=session.get("session_variables"))

# The Adress Form Part 5


@app.route('/<string:lang>/gez/adress5', methods=['GET', 'POST'])
def adress5(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Phone Nr.
        POSTname = get_POST_name(10)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(10)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods1')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
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
        POSTname = get_POST_name(11)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(11)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods2')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/payment_methods1')
        return render_template(language_glob + '/payment_methods/payment_methods1.html', language=language_glob, fields=session.get("session_variables"))


# The Payment Methods Form Part 2
@app.route('/<string:lang>/gez/payment_methods2', methods=['GET', 'POST'])
def payment_methods2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Type of Transfer.
        POSTname = get_POST_name(12)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(12)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        if request.form["type"] == "sepa":
            return redirect('/' + language_glob + '/gez/sepa1')
        elif request.form["type"] == "bank":
            return redirect('/' + language_glob + '/gez/final')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
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
        POSTname = get_POST_name(13)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(13)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa2')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa1')
        return render_template(language_glob + '/sepa/sepa1.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 2
@app.route('/<string:lang>/gez/sepa2', methods=['GET', 'POST'])
def sepa2(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # Street.
        POSTname = get_POST_name(14)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(14)
        fill_SV_and_DB(POSTname, var_POST)
        # Street Nr.
        POSTname = get_POST_name(15)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(15)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa3')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa2')
        return render_template(language_glob + '/sepa/sepa2.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 3
@app.route('/<string:lang>/gez/sepa3', methods=['GET', 'POST'])
def sepa3(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # ZIP.
        POSTname = get_POST_name(16)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(16)
        fill_SV_and_DB(POSTname, var_POST)
        # City.
        POSTname = get_POST_name(17)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(17)
        fill_SV_and_DB(POSTname, var_POST)
        #################################################
        return redirect('/' + language_glob + '/gez/sepa4')
    else:
        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa3')
        return render_template(language_glob + '/sepa/sepa3.html', language=language_glob, fields=session.get("session_variables"))


# The Sepa Form Part 4
@app.route('/<string:lang>/gez/sepa4', methods=['GET', 'POST'])
def sepa4(lang):
    language_glob = session.get("lang")

    if request.method == 'POST':
        ########## Extract Data From Fields ##########
        # IBAN.
        POSTname = get_POST_name(18)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(18)
        fill_SV_and_DB(POSTname, var_POST)
        # BIC.
        POSTname = get_POST_name(19)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(19)
        fill_SV_and_DB(POSTname, var_POST)
        # Credit Institution.
        POSTname = get_POST_name(20)
        var_POST = request.form[POSTname]
        POSTname = get_session_name(20)
        fill_SV_and_DB(POSTname, var_POST)

        sv = session.get("session_variables")
        fill_pdf(sv)
        #################################################
        return redirect('/' + language_glob + '/gez/final')

    else:

        if request.args.get('lang') != None:
            change_lang(request.args.get('lang'))
            return redirect('/' + request.args.get('lang') + '/gez/sepa4')
        return render_template(language_glob + '/sepa/sepa4.html', language=language_glob, fields=session.get("session_variables"))

# Final notice page for GEZ


@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        change_lang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/gez/final')
    return render_template(language_glob + '/final.html', language=language_glob)


# About us page
@app.route('/<string:lang>/about_us')
def about(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        change_lang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/about_us')
    return render_template(language_glob + '/about_us.html', language=language_glob)

# Privacy policy


@app.route('/<string:lang>/privacy_policy')
def privacy_policy(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        change_lang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/privacy_policy')
    return render_template(language_glob + '/privacy_policy.html', language=language_glob)

# Legal notice


@app.route('/<string:lang>/legal_notice')
def legal_notice(lang):
    language_glob = session.get("lang")

    if request.args.get('lang') != None:
        change_lang(request.args.get('lang'))
        return redirect('/' + request.args.get('lang') + '/legal_notice')
    return render_template(language_glob + '/legalNotice.html', language=language_glob)


if __name__ == "__main__":
    app.secret_key = str(os.urandom(12))
    app.run(debug=True)

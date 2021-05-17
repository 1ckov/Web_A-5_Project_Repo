from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#db = SQLAlchemy(app)

language_glob = "en"

# "Chose language" and "Loggin" page
@app.route('/')

def index():
    return render_template(language_glob + '/welcome.html')

# Registration Page 
@app.route('/<string:lang>/register', methods=['GET','POST'])
def registration():
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        language_glob = request.form['language']
        #################################################
        return redirect('/' + language_glob + '/home')
    else:
        return render_template( language_glob + '/register.html')

# Landing Page for each language
@app.route('/<string:lang>/home')
def home(lang):
    global language_glob
    if request.args.get('lang') != None:
        return redirect ('/' + request.args.get('lang') + '/home')
    language_glob = lang
    print (language_glob)
    return render_template(language_glob + '/home.html', language = language_glob)

# The GEZ Form Part 1 (Generall information)
@app.route('/<string:lang>/gez/general_information', methods=['GET','POST'])
def general_information(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress' )
    else:
        if request.args.get('lang') != None:
            return redirect ('/' + request.args.get('lang') + '/gez/general_information')
        language_glob = lang
        print (language_glob)
        return render_template(language_glob + '/general_information.html', language = lang)

# The GEZ Form Part 2 (Adress)
@app.route('/<string:lang>/gez/adress', methods=['GET','POST'])
def adress(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods' )
    else:
        if request.args.get('lang') != None:
            return redirect ('/' + request.args.get('lang') + '/gez/adress')
        language_glob = lang
        return render_template(language_glob + '/adress.html', language = language_glob)

# The GEZ Form Part 4 (Payment Methods)
@app.route('/<string:lang>/gez/payment_methods', methods=['GET','POST']) 
def payment_methods(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        
        #################################################
        if request.form["type"] == "sepa":
            return redirect('/' + language_glob + '/gez/sepa' )
        elif request.form["type"] == "bank":
            return redirect('/' + language_glob + '/gez/final')
    else:
        if request.args.get('lang') != None:
            return redirect ('/' + request.args.get('lang') + '/gez/payment_methods')
        language_glob = lang
        return render_template(language_glob + '/payment_methods.html', language = language_glob)

# The GEZ Form Part 5 (Sepa Data)
@app.route('/<string:lang>/gez/sepa', methods=['GET','POST'])
def sepa(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/final' )
    else:
        if request.args.get('lang') != None:
            return redirect ('/' + request.args.get('lang') + '/gez/sepa')
        language_glob = lang
        return render_template(language_glob + '/sepa.html', language = language_glob)

# Final notice page for GEZ
@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    global language_glob
    if request.args.get('lang') != None:
        return redirect ('/' + request.args.get('lang') + '/gez/final')
    language_glob = lang
    return render_template(language_glob + '/final.html')

# About us page
@app.route('/<string:lang>/about')
def about(lang):
    global language_glob
    if request.args.get('lang') != None:
        return redirect ('/' + request.args.get('lang') + '/about')
    language_glob = lang
    return render_template(language_glob + '/about_us.html', language = language_glob)

if __name__ == "__main__":
    app.run(debug=True)
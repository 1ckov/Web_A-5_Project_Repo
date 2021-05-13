from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#db = SQLAlchemy(app)
   
language = "en"

# "Chose language" and "Loggin" page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        language = request.form['language']
        #################################################
        return redirect('/' + language + '/home' )
    else:
        return render_template('register.html')

# Landing Page for each language
@app.route('/<string:lang>/home')
def home(lang):
    return render_template(lang + '/home.html', language = lang)

# The GEZ Form Part 1 (Generall information)
@app.route('/<string:lang>/gez/general_information', methods=['GET','POST'])
def general_information(lang):
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + lang + '/gez/adress' )
    else:
        return render_template(lang + '/general_information.html', language = lang)

# The GEZ Form Part 2 (Adress)
@app.route('/<string:lang>/gez/adress', methods=['GET','POST'])
def adress(lang):
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + lang + '/gez/payment_methods' )
    else:
        return render_template(lang + '/adress.html', language = lang)

# The GEZ Form Part 4 (Payment Methods)
@app.route('/<string:lang>/gez/payment_methods', methods=['GET','POST']) 
def payment_methods(lang):
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + lang + '/gez/sepa' )
    else:
        return render_template(lang + '/payment_methods.html', language = lang)

# The GEZ Form Part 5 (Sepa Data)
@app.route('/<string:lang>/gez/sepa', methods=['GET','POST'])
def sepa(lang):
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + lang + '/gez/final' )
    else:
        return render_template(lang + '/sepa.html', language = lang)

@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    return render_template(lang + '/final.html')


@app.route('/<string:lang>/about')
def about(lang):
    return render_template(lang + '/about_us.html', language = lang)

if __name__ == "__main__":
    app.run(debug=True)
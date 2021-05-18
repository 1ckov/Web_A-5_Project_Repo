from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#db = SQLAlchemy(app)

language_glob = "en"

# "Chose language" and "Loggin" page

@app.route('/', methods=['GET','POST'])
def index():
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########

        #################################################
        return redirect('/' + language_glob + '/home')
    
    if request.args.get('lang') != None:
        language_glob = request.args.get('lang')
        return redirect('/')
    return render_template(language_glob + '/welcome.html', language = language_glob)

# Registration Page 
@app.route('/<string:lang>/register', methods=['GET','POST'])
def registration(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        language_glob = request.form['language']

        #################################################
        return redirect('/' + language_glob + '/home')
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + language_glob + '/register')
        return render_template( language_glob + '/register.html', language = language_glob)

# Landing Page for each language
@app.route('/<string:lang>/home')
def home(lang):
    global language_glob
    if request.args.get('lang') != None:
        language_glob = request.args.get('lang')
        return redirect('/' + language_glob + '/home')
    return render_template(language_glob + '/home.html', language = language_glob)

# GEZ Explanation
@app.route('/<string:lang>/gez/gez_explanation', methods=['GET','POST'])
def gez_explanation(lang):
    global language_glob
    if request.method == 'POST':
        return redirect('/' + language_glob + '/gez/general_information1')
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez_explanation')
        return render_template(language_glob + '/gez_explanation.html', language = language_glob)

########################################################################################
###################################### General Information #############################
########################################################################################

# The General information Form Part 1
@app.route('/<string:lang>/gez/general_information1', methods=['GET','POST'])
def general_information1(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/general_information2' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/general_information1')
        return render_template(language_glob + '/general_information/general_information1.html', language = language_glob)

# The General information Form Part 2
@app.route('/<string:lang>/gez/general_information2', methods=['GET','POST'])
def general_information2(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/general_information3' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/general_information2')
        return render_template(language_glob + '/general_information/general_information2.html', language = language_glob)

# The General information Form Part 3
@app.route('/<string:lang>/gez/general_information3', methods=['GET','POST'])
def general_information3(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress1' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/general_information3')
        return render_template(language_glob + '/general_information/general_information3.html', language = language_glob)

########################################################################################
###################################### Adress ##########################################
########################################################################################

# The Adress Form Part 1 
@app.route('/<string:lang>/gez/adress1', methods=['GET','POST'])
def adress1(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress2' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/adress1')
        return render_template(language_glob + '/adress/adress1.html', language = language_glob)

# The Adress Form Part 2 
@app.route('/<string:lang>/gez/adress2', methods=['GET','POST'])
def adress2(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress3' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/adress2')
        return render_template(language_glob + '/adress/adress2.html', language = language_glob)

# The Adress Form Part 3 
@app.route('/<string:lang>/gez/adress3', methods=['GET','POST'])
def adress3(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress4' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/adress3')
        return render_template(language_glob + '/adress/adress3.html', language = language_glob)

# The Adress Form Part 4 
@app.route('/<string:lang>/gez/adress4', methods=['GET','POST'])
def adress4(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/adress5' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/adress4')
        return render_template(language_glob + '/adress/adress4.html', language = language_glob)

# The Adress Form Part 5 
@app.route('/<string:lang>/gez/adress5', methods=['GET','POST'])
def adress5(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/payment_methods1' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/adress5')
        return render_template(language_glob + '/adress/adress5.html', language = language_glob)

########################################################################################
############################### Payment Methods ########################################
########################################################################################

# The Payment Methods Form Part 1
@app.route('/<string:lang>/gez/payment_methods1', methods=['GET','POST']) 
def payment_methods1(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        
        #################################################
            return redirect('/' + language_glob + '/gez/payment_methods2')
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/payment_methods1')
        return render_template(language_glob + '/payment_methods/payment_methods1.html', language = language_glob)


# The Payment Methods Form Part 2
@app.route('/<string:lang>/gez/payment_methods2', methods=['GET','POST']) 
def payment_methods2(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        
        #################################################
        if request.form["type"] == "sepa":
            return redirect('/' + language_glob + '/gez/sepa1' )
        elif request.form["type"] == "bank":
            return redirect('/' + language_glob + '/gez/final')
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/payment_methods2')
        return render_template(language_glob + '/payment_methods/payment_methods2.html', language = language_glob)

########################################################################################
###################################### Sepa ############################################
########################################################################################

# The Sepa Form Part 1
@app.route('/<string:lang>/gez/sepa1', methods=['GET','POST'])
def sepa1(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa2' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/sepa1')
        return render_template(language_glob + '/sepa/sepa1.html', language = language_glob)


# The Sepa Form Part 2
@app.route('/<string:lang>/gez/sepa2', methods=['GET','POST'])
def sepa2(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa3' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/sepa2')
        return render_template(language_glob + '/sepa/sepa2.html', language = language_glob)


# The Sepa Form Part 3
@app.route('/<string:lang>/gez/sepa3', methods=['GET','POST'])
def sepa3(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/sepa4' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/sepa3')
        return render_template(language_glob + '/sepa/sepa3.html', language = language_glob)


# The Sepa Form Part 4
@app.route('/<string:lang>/gez/sepa4', methods=['GET','POST'])
def sepa4(lang):
    global language_glob
    if request.method == 'POST':
        ########## Put data from forms into DB ##########
        
        #################################################
        return redirect('/' + language_glob + '/gez/final' )
    else:
        if request.args.get('lang') != None:
            language_glob = request.args.get('lang')
            return redirect ('/' + request.args.get('lang') + '/gez/sepa4')
        return render_template(language_glob + '/sepa/sepa4.html', language = language_glob)

# Final notice page for GEZ
@app.route('/<string:lang>/gez/final')
def gez_final(lang):
    global language_glob
    if request.args.get('lang') != None:
        language_glob = request.args.get('lang')
        return redirect ('/' + request.args.get('lang') + '/gez/final')
    return render_template(language_glob + '/final.html')

# About us page
@app.route('/<string:lang>/about_us')
def about(lang):
    global language_glob
    if request.args.get('lang') != None:
        language_glob = request.args.get('lang')
        return redirect ('/' + request.args.get('lang') + '/about')
    return render_template(language_glob + '/about_us.html', language = language_glob)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

#Types of errors that may occur

def empty_form(a_string):
    if a_string == "":
        return True
    else:
        return False

def contains_space(a_string):
    if " " in a_string:
        return True
    else:
        return False

def length_failure(a_string):
    if len(a_string) < 3 or len(a_string) > 20:
        return True
    else:
        return False

def verification_failure(string1, string2):
    if string1 != string2:
        return True
    else:
        return False

def not_one_at_symbol(string1):
    if string1.count("@") != 1:
        return True
    else:
        return False

def not_one_period(string1):
    if string1.count(".") != 1:
        return True
    else:
        return False

@app.route('/register')
def display_signup_form():
    return render_template('signup_form.html' )

@app.route('/register', methods=['POST'])
def signup_request():
    username = request.form['username']
    passcode = request.form['passcode']
    verify = request.form['verify']
    email = request.form['email']

    verify_error = ""
    passcode_error = ""
    username_error = ""
    email_error = ""
    pass_lock = 0

    #username verification
    if empty_form(username):
        username_error = "Required field"
        pass_lock = 1
    elif contains_space(username):
        username_error = "Username cannot contain spaces"
        pass_lock = 1
    elif length_failure(username):
        username_error = "Username must be 3-20 characters"
        pass_lock = 1
    else:
        username_error = ""
    
    #password verification
    if empty_form(passcode):
        passcode_error = "Required field"
        pass_lock = 1
    elif contains_space(passcode):
        passcode_error = "Password cannot contain spaces"
        pass_lock = 1
    elif length_failure(passcode):
        passcode_error = "Password must be 3-20 characters"
        pass_lock = 1
    else:
        passcode_error = ""

    #verify password verification
    if empty_form(verify):
        verify_error = "Required field"
        pass_lock = 1
    elif verification_failure(verify, passcode):
        verify_error = "Passwords must match" 
        pass_lock = 1
    else:
        verify_error = ""
    
    #checks if there is anytext in email form
    if not empty_form(email):
        #email verification
        if not_one_at_symbol(email):
            email_error = "Invalid email address"
            pass_lock = 1
        elif not_one_period(email):
            email_error = "Invalid email address"
            pass_lock = 1
        elif length_failure(email):
            email_error = "Email must be 3-20 characters"
            pass_lock = 1
    
    #if pass_lock is (1)ocked and not (0)pen, will display error messages on "/"
    if pass_lock == 1:
        return render_template('signup_form.html', verify_error = verify_error,
        passcode_error = passcode_error, username_error = username_error, email_error = email_error,
        username = username, email = email)
    else:
        return redirect('/welcome?username={0}'.format(username))

@app.route("/welcome")
def welcome_user():
    username = request.args.get('username')
    return render_template('welcome.html', username = username)
app.run()